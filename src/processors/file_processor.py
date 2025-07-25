class FileProcessor():

    @staticmethod
    def process(fileName):
        f = open(fileName)
        gridSize = f.readline().rstrip().split(' ')
        instructions = {} 
        instructions['gridSize'] = {} 
        instructions['gridSize']['x'] = gridSize[0]
        instructions['gridSize']['y'] = gridSize[1]
        instructions['robotGuidance'] = []
        while True:
            robotStartingPosition = f.readline()
            robotInstructionsString = f.readline()
            startingPositionFormatted = robotStartingPosition.rstrip().split(' ')
            if len(startingPositionFormatted) != 3: 
                break
            robotInstructions = {}
            robotInstructions['startingPosition'] = {}
            robotInstructions['startingPosition']['x'] = startingPositionFormatted[0]
            robotInstructions['startingPosition']['y'] = startingPositionFormatted[1]
            robotInstructions['startingPosition']['direction'] = startingPositionFormatted[2]
            robotInstructions['instructions'] = list(robotInstructionsString.rstrip())
            instructions['robotGuidance'].append(robotInstructions)
            if not robotInstructionsString: break  # EOF
        return instructions 