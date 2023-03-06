import type {DatasetDTO} from './ml/dataset-dto';
import type {ModelDTO} from './ml/model-dto';
import type {TestFunctionDTO} from './test-function-dto';
import type {TestSuiteExecutionDTO} from './ml/test-suite-execution-dto';
import type {TestSuiteNewDTO} from './test-suite-new-dto';

/**
 * Generated from ai.giskard.web.dto.TestSuiteCompleteDTO
 */
export interface TestSuiteCompleteDTO {
    datasets: DatasetDTO[];
    executions: TestSuiteExecutionDTO[];
    inputs: {[key: string]: string};
    models: ModelDTO[];
    registry: TestFunctionDTO[];
    suite: TestSuiteNewDTO;
}