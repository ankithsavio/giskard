from unittest.mock import Mock

import numpy as np
import pandas as pd
from bokeh.plotting import figure

from giskard.rag import QATestset, RAGReport
from giskard.rag.knowledge_base import KnowledgeBase
from tests.rag.test_qa_testset import make_testset_df


def test_report_plots():
    knowledge_base = Mock()

    testset = QATestset(make_testset_df())

    eval_results = [
        {"evaluation": True, "reason": "The assistant answer is correct.", "assistant_answer": "Default answer"},
        {"evaluation": True, "reason": "The assistant answer is correct.", "assistant_answer": "Default answer"},
        {"evaluation": False, "reason": "The assistant answer is incorrect.", "assistant_answer": "Default answer"},
        {"evaluation": True, "reason": "The assistant answer is correct.", "assistant_answer": "Default answer"},
        {"evaluation": False, "reason": "The assistant answer is incorrect.", "assistant_answer": "Default answer"},
        {"evaluation": False, "reason": "The assistant answer is incorrect.", "assistant_answer": "Default answer"},
    ]

    metrics_results = {
        "context_precision": pd.DataFrame.from_dict(
            {"id": ["1", "2", "3", "4", "5", "6"], "context_precision": [0.1] * 6}
        ),
        "faithfulness": pd.DataFrame.from_dict({"id": ["1", "2", "3", "4", "5", "6"], "faithfulness": [0.2] * 6}),
        "answer_relevancy": pd.DataFrame.from_dict(
            {"id": ["1", "2", "3", "4", "5", "6"], "answer_relevancy": [0.3] * 6}
        ),
        "context_recall": pd.DataFrame.from_dict({"id": ["1", "2", "3", "4", "5", "6"], "context_recall": [0.4] * 6}),
    }

    report = RAGReport(eval_results, testset, knowledge_base, metrics_results=metrics_results)
    print(report._dataframe)
    print(report._dataframe.columns)
    plot = report.plot_correctness_by_metadata(metadata_name="question_type")
    assert isinstance(plot, figure)

    plot = report.plot_metrics_hist("context_precision", filter_metadata={"question_type": ["EASY"]})
    assert isinstance(plot, figure)

    histograms = report.get_metrics_histograms()
    assert "Overall" in histograms
    assert "Question" in histograms
    assert "Topics" in histograms

    assert len(histograms["Overall"]["Overall"]) == 4
    assert len(histograms["Question"]) == 4
    assert len(histograms["Topics"]) == 2
    assert len(histograms["Topics"]["Cheese_1"]) == 4
    assert len(histograms["Question"]["EASY"]) == 4


def test_report_save_load(tmp_path):
    df = make_testset_df()
    llm_client = Mock()
    llm_client.embeddings = Mock()
    llm_client.embeddings.return_value = np.random.randn(len(df), 8)

    knowledge_base = KnowledgeBase(df, llm_client=llm_client)
    knowledge_base._topics_inst = {0: "Cheese_1", 1: "Cheese_2"}
    for doc_idx, doc in enumerate(knowledge_base._documents):
        if doc_idx < 3:
            doc.topic_id = 0
        else:
            doc.topic_id = 1

    knowledge_base._documents

    testset = QATestset(make_testset_df())

    eval_results = [
        {"evaluation": True, "reason": "The assistant answer is correct.", "assistant_answer": "Default answer"},
        {"evaluation": True, "reason": "The assistant answer is correct.", "assistant_answer": "Default answer"},
        {"evaluation": False, "reason": "The assistant answer is incorrect.", "assistant_answer": "Default answer"},
        {"evaluation": True, "reason": "The assistant answer is correct.", "assistant_answer": "Default answer"},
        {"evaluation": False, "reason": "The assistant answer is incorrect.", "assistant_answer": "Default answer"},
        {"evaluation": False, "reason": "The assistant answer is incorrect.", "assistant_answer": "Default answer"},
    ]

    metrics_results = {
        "context_precision": pd.DataFrame.from_dict(
            {"id": ["1", "2", "3", "4", "5", "6"], "context_precision": [0.1] * 6}
        ),
        "faithfulness": pd.DataFrame.from_dict({"id": ["1", "2", "3", "4", "5", "6"], "faithfulness": [0.2] * 6}),
        "answer_relevancy": pd.DataFrame.from_dict(
            {"id": ["1", "2", "3", "4", "5", "6"], "answer_relevancy": [0.3] * 6}
        ),
        "context_recall": pd.DataFrame.from_dict({"id": ["1", "2", "3", "4", "5", "6"], "context_recall": [0.4] * 6}),
    }

    report = RAGReport(eval_results, testset, knowledge_base, metrics_results=metrics_results)

    report.save(tmp_path)
    loaded_report = RAGReport.load(tmp_path, llm_client=llm_client)

    assert all(
        [
            doc.content == loaded_doc.content
            for doc, loaded_doc in zip(report._knowledge_base._documents, loaded_report._knowledge_base._documents)
        ]
    )
    assert report._knowledge_base.topics == loaded_report._knowledge_base.topics

    assert len(report._testset._dataframe) == len(loaded_report._testset._dataframe)
    assert len(report._metrics_results) == len(loaded_report._metrics_results)
    assert (
        report._metrics_results["context_precision"].loc[0, "context_precision"]
        == loaded_report._metrics_results["context_precision"].loc[0, "context_precision"]
    )
    assert report._results[0]["evaluation"] == loaded_report._results[0]["evaluation"]
    assert report._results[0]["reason"] == loaded_report._results[0]["reason"]
    assert report._results[0]["assistant_answer"] == loaded_report._results[0]["assistant_answer"]