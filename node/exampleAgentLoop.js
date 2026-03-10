const { RunGovernor } = require("./runGovernor")

const governor = new RunGovernor()

for (let i = 0; i < 10; i++) {

  governor.recordStep()

  console.log("agent step", i)

}
