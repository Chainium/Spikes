pipeline {
  agent any
  stages {
	stage('Build') {
	  steps {
		sh 'dotnet build $SOLUTION_NAME -c $BUILD_CONFIG -o $PROJECT_OUTPUT_FOLDER'
	  }
	}
	stage('Unit tests') {
	  environment {
		RESULTS_OUTPUT_PATH = '/testresults'
	  }
	  steps {
		sh 'bash ./Build/run_tests.sh $SOLUTION_NAME $BUILD_CONFIG $PROJECT_OUTPUT_FOLDER $RESULTS_OUTPUT_PATH *.Tests*'
		xunit testTimeMargin: '3000', thresholdMode: 1, thresholds: [failed(failureNewThreshold: '0', failureThreshold: '0', unstableNewThreshold: '0', unstableThreshold: '0'), skipped(failureNewThreshold: '0', failureThreshold: '0', unstableNewThreshold: '0', unstableThreshold: '0')], tools: [MSTest(deleteOutputFiles: true, failIfNotNew: true, pattern: '$TEST_RESULTS_PATH/**', skipNoTestFiles: false, stopProcessingIfError: true)]
	  }
	}
  }
  environment {
	SOLUTION_NAME = 'Simplify'
	BUILD_CONFIG = 'Release'
	PROJECT_OUTPUT_FOLDER = 'Release'
  }
}