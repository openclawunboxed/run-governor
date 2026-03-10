from run_governor import RunGovernor

def run_agent():
    gov = RunGovernor()

    for i in range(10):
        gov.record_step()
        gov.record_tool()

        print("agent step", i)

if __name__ == "__main__":
    run_agent()
