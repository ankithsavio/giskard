from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import os
import random
import string
import tempfile
import warnings
from pathlib import Path

import pandas as pd

from giskard.core.errors import GiskardImportError
from giskard.llm import get_default_client
from giskard.llm.client import LLMMessage
from giskard.utils.analytics_collector import analytics, anonymize

if TYPE_CHECKING:
    from mlflow import MlflowClient


class ScanReport:
    def __init__(self, issues, model=None, dataset=None, as_html: bool = True):
        """The scan report contains the results of the scan.

        Note that this object is not meant to be instantiated directly. Instead, it is returned by the
        :func:`giskard.scan`. See :class:`Scanner` for more details.

        Parameters
        ----------
        issues : list
            A list of :class:`Issue` objects.
        model : BaseModel
            A Giskard model object.
        dataset : Dataset
            A Giskard dataset object.
        as_html : bool
            Whether to render the report widget as HTML.
        """
        self.issues = issues
        self.as_html = as_html
        self.model = model
        self.dataset = dataset

    def has_issues(self):
        return len(self.issues) > 0

    def __repr__(self):
        if not self.has_issues():
            return "<ScanReport (no issues)>"

        return f"<ScanReport ({len(self.issues)} issue{'s' if len(self.issues) > 1 else ''})>"

    def _ipython_display_(self):
        if self.as_html:
            from IPython.core.display import display_html

            html = self._repr_html_()
            display_html(html, raw=True)
        else:
            from IPython.core.display import display_markdown

            markdown = self._repr_markdown_()
            display_markdown(markdown, raw=True)

    def _repr_html_(self):
        return self.to_html(embed=True)

    def _repr_markdown_(self):
        return self.to_markdown()

    def to_html(self, filename=None, embed=False):
        """Renders the scan report as HTML.

        Saves or returns the HTML representation of the scan report.

        Parameters
        ----------
        filename : Optional[str]
            If provided, the HTML will be written to the file.
        embed : Optional[bool]
            Whether to configure the HTML to be embedded in an iframe.
        """
        from ..visualization.widget import ScanReportWidget

        widget = ScanReportWidget(self)

        with pd.option_context("display.max_colwidth", None):
            html = widget.render_html(embed=embed)

        if filename is not None:
            with open(filename, "w") as f:
                f.write(html)
            return

        return html

    def to_doc(self, dir: Optional[str] = "doc_scan", llm_based: Optional[bool] = False):
        """
        Generates a doc from the scan report results

        Parameters
        ----------
        dir : Optional[str]
            If provided, the docs will be written in the specified folder.
        llm_based : Optional[bool]
            Whether to generate further content with an LLM or to stick to the basic information.
        """

        def generate_prompt(report_content, result_test):
            return f"""

            You are an AI reading and summarizing tool made to allow non expert people in a company to understand technical reports about machine learning models. Your mission is to understand a report which analyzes the behavior of a machine learning model.

            Report:

            {report_content}

            ----------------

            The requirement is: {result_test}

            ----------------

            Start by explicitly mentioning if the model passed the requirement or not.

            Then, provide a summary of the report and explain the issues found by sticking
            to the content of the report. You must not extrapolate, you should stick to the facts.
            You must make it as understandable as possible to non expert people and not relate
            to anything else than the report.
            Provide enough details so that it is easy to understand.

            List the issues found as follows:
            - Issue 1: ...
            - Issue 2: ...
            ...

            If the model failed to pass the test, explicitly mention why.
            Otherwise, if the model passed the test, state that the test is a success
            and explain the other issues that can be fixed to further improve it.

            Factual and easy to understand summary of the report for non expert people:

            """

        # Get default llm
        llm = get_default_client() if llm_based else None

        # Group issues by type
        issue_groups = {}
        for elt in self.issues:
            if elt.group.name not in issue_groups:
                issue_groups[elt.group.name] = {"description": elt.group.description, "issues": []}
            issue_groups[elt.group.name]["issues"].append({"level": elt.level.value, "description": elt.description})

        # Create simple report content from issue group name anddescription,
        # and issues level and description
        content_issues = {}
        for issue_group in issue_groups:
            current_content = f"Category: {issue_group} \n\n"
            current_content += f"Description: {issue_groups[issue_group]['description']} \n\n"
            for issue in issue_groups[issue_group]["issues"]:
                current_content += f"LEVEL {issue['level']} - {issue['description']}\n"
            content_issues[issue_group] = current_content

        # Generate complete report
        results = {}
        for issue_group in content_issues:
            results[issue_group] = {
                "status": 0 if "major" in content_issues[issue_group] else 1,
                "summary": llm.complete(
                    [
                        LLMMessage(
                            role="user",
                            content=generate_prompt(
                                content_issues[issue_group],
                                "failed" if "major" in content_issues[issue_group] else "passed",
                            ),
                        )
                    ]
                ).content
                if llm_based
                else content_issues[issue_group],
            }

        final_results = {"context_requirement": [], "rejection_reason": [], "checklist": []}

        for elt in results:
            final_results["context_requirement"].append(results[elt]["status"])
            final_results["rejection_reason"].append(results[elt]["summary"])
            final_results["checklist"].append(elt)

        final_results = pd.DataFrame(final_results)

        # Create folder and markdown documents from generated reports
        os.makedirs(dir, exist_ok=True)

        for _, row in final_results.iterrows():
            content_md = f"## Requirement on {row['checklist']}\n\n"
            content_md += f"### Requirement result: **{'Passed' if row['context_requirement'] else 'Failed'}**\n\n"
            content_md += row["rejection_reason"]

            with open(f"{dir}/{row['checklist']}.md", "w") as filename:
                filename.write(content_md)

        return

    def to_markdown(self, filename=None, template="summary"):
        """Renders the scan report as markdown.

        Saves or returns the markdown representation of the scan report.

        Parameters
        ----------
        filename : Optional[str]
            If provided, the markdown will be written to the file.
        template : Optional[str]
            The template to use. Currently, only ``summary`` is supported.
        """
        from ..visualization.widget import ScanReportWidget

        widget = ScanReportWidget(self)
        markdown = widget.render_markdown(template=template)

        if filename is not None:
            with open(filename, "w") as f:
                f.write(markdown)
            return

        return markdown

    def to_dataframe(self):
        """Returns the scan report as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the scan report details.
        """
        df = pd.DataFrame(
            [
                {
                    "domain": issue.meta.get("domain"),
                    "slicing_fn": str(issue.slicing_fn) if issue.slicing_fn else None,
                    "transformation_fn": str(issue.transformation_fn) if issue.transformation_fn else None,
                    "metric": issue.meta.get("metric"),
                    "deviation": issue.meta.get("deviation"),
                    "description": issue.description,
                }
                for issue in self.issues
            ]
        )
        return df

    def generate_tests(self, with_names=False):
        """Automatically generates tests from the scan results.

        This method provides a way to generate a list of tests automatically, based on the issues detected by the scan.
        Usually you will want to generate a test suite directly, see :meth:`generate_test_suite` for more details.

        Parameters
        ----------
        with_names : Optional[bool]
            Whether to return the test names as well. If ``True``, the method will return a list of tuples.

        Return
        ------
        list
            A list of Giskard test objects.
        """
        tests = sum([issue.generate_tests(with_names=with_names) for issue in self.issues], [])
        return tests

    def generate_test_suite(self, name=None):
        """Automatically generates a test suite from the scan results.

        This method provides a way to generate a test suite automatically, based on the issues detected by the scan.
        The test suite can be used to reproduce the issues and can be uploaded to the Giskard Hub for debugging.

        Parameters
        ----------
        name : Optional[str]
            The name of the test suite. If not provided, a default name will be used. You can also change the name
            later by accessing the ``name`` attribute of the returned test suite.

        Return
        ------
        Suite
            A test suite containing tests from the scan results.
        """
        from giskard.core.suite import Suite

        # Set suite-level default parameters if exists
        suite_default_params = {}
        if self.model:
            suite_default_params.update({"model": self.model})
        if self.dataset:
            suite_default_params.update({"dataset": self.dataset})

        suite = Suite(name=name or "Test suite (generated by automatic scan)", default_params=suite_default_params)
        for test, test_name in self.generate_tests(with_names=True):
            suite.add_test(test, test_name, test_name)

        self._track_suite(suite, name)
        return suite

    def _track_suite(self, suite, name):
        tests_cnt = {}
        if suite.tests:
            for t in suite.tests:
                try:
                    name = t.giskard_test.meta.full_name
                    if name not in tests_cnt:
                        tests_cnt[name] = 1
                    else:
                        tests_cnt[name] += 1
                except:  # noqa
                    pass
        analytics.track(
            "scan:generate_test_suite",
            {"suite_name": anonymize(name), "tests_cnt": len(suite.tests), **tests_cnt},
        )

    @staticmethod
    def get_scan_summary_for_mlflow(scan_results):
        results_df = scan_results.to_dataframe()
        if "metric" in results_df.columns:
            results_df.metric = results_df.metric.replace("=.*", "", regex=True)
        return results_df

    def to_mlflow(
        self,
        mlflow_client: MlflowClient = None,
        mlflow_run_id: str = None,
        summary: bool = True,
        model_artifact_path: str = "",
    ):
        """Logs the scan results to MLflow.

        Log the current scan results in an HTML format to the active MLflow run.
        """
        import mlflow

        results_df = self.get_scan_summary_for_mlflow(self)
        if model_artifact_path != "":
            model_artifact_path = "-for-" + model_artifact_path

        with tempfile.NamedTemporaryFile(
            prefix="giskard-scan-results" + model_artifact_path + "-", suffix=".html", delete=False
        ) as f:
            # Get file path
            scan_results_local_path = f.name
            # Get name from file
            scan_results_artifact_name = Path(f.name).name
            scan_summary_artifact_name = "scan-summary" + model_artifact_path + ".json" if summary else None
            # Write the file on disk
            self.to_html(scan_results_local_path)

        try:
            if mlflow_client is None and mlflow_run_id is None:
                mlflow.log_artifact(scan_results_local_path)
                if summary:
                    mlflow.log_table(results_df, artifact_file=scan_summary_artifact_name)
            elif mlflow_client and mlflow_run_id:
                mlflow_client.log_artifact(mlflow_run_id, scan_results_local_path)
                if summary:
                    mlflow_client.log_table(mlflow_run_id, results_df, artifact_file=scan_summary_artifact_name)
        finally:
            # Force deletion of the temps file
            Path(f.name).unlink(missing_ok=True)

        return scan_results_artifact_name, scan_summary_artifact_name

    def to_wandb(self, run: Optional["wandb.wandb_sdk.wandb_run.Run"] = None) -> None:  # noqa
        """Logs the scan results to the WandB run.

        Log the current scan results in an HTML format to the active WandB run.

        Parameters
        ----------
        run :
            WandB run.
        """
        try:
            import wandb  # noqa
        except ImportError as e:
            raise GiskardImportError("wandb") from e
        from ..integrations.wandb.wandb_utils import get_wandb_run

        run = get_wandb_run(run)
        try:
            html = self.to_html()
            suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
            wandb_artifact_name = f"Vulnerability scan results/giskard-scan-results-{suffix}"
            analytics.track(
                "wandb_integration:scan_result",
                {
                    "wandb_run_id": run.id,
                    "has_issues": self.has_issues(),
                    "issues_cnt": len(self.issues),
                },
            )
        except Exception as e:
            analytics.track(
                "wandb_integration:scan_result:error:unknown",
                {
                    "wandb_run_id": run.id,
                    "error": str(e),
                },
            )
            raise RuntimeError(
                "An error occurred while logging the scan results into wandb. "
                "Please submit the traceback as a GitHub issue in the following "
                "repository for further assistance: https://github.com/Giskard-AI/giskard."
            ) from e

        run.log({wandb_artifact_name: wandb.Html(html, inject=False)})

    def to_avid(self, filename=None):
        """Renders the scan report as an AVID report.

        Saves or returns the AVID representation of the scan report.

        Parameters
        ----------
        filename : Optional[str]
            If provided, the AVID report will be written to the file.
        """
        from ..integrations import avid

        reports = [
            avid.create_report_from_issue(issue=issue, model=self.model, dataset=self.dataset) for issue in self.issues
        ]

        if filename is not None:
            with open(filename, "w") as f, warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)  # we need to support both pydantic 1 & 2
                f.writelines(r.json() + "\n" for r in reports)
            return

        return reports
