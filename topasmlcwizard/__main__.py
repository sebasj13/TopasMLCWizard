import topasmlcwizard.topasmlcwizard as topasmlcwizard
import sys

if len(sys.argv) > 1:
    topasmlcwizard.MLCWizard(sys.argv[1])
else:
    topasmlcwizard.MLCWizard()