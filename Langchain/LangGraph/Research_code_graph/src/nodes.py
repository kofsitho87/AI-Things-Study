from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
import functools
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
load_dotenv()


tavily_tool = TavilySearchResults(max_results=5)

members = ["Researcher", "Coder"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
options = ["FINISH"] + members


class Nodes():
    llm: ChatOpenAI

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def _create_agent(self, llm: ChatOpenAI, tools: list, system_prompt: str):
        # Each worker node will be given a name and some tools.
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools)
        return executor
    
    def _agent_node(self, state, agent, name):
        result = agent.invoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}
        

    def supervisor_chain_node(self, llm=None):
        function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": options},
                        ],
                    }
                },
                "required": ["next"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))

        llm = llm or self.llm

        supervisor_chain = (
            prompt
            | llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )
        return supervisor_chain
    
    def code_node(self, llm=None):
        python_repl_tool = PythonREPLTool()

        llm = llm or self.llm

        code_agent = self._create_agent(
            llm,
            [python_repl_tool],
            "You may generate safe python code to analyze data and generate charts using matplotlib.",
        )
        code_node = functools.partial(self._agent_node, agent=code_agent, name="Coder")
        return code_node


    def research_node(self, llm=None):
        llm = llm or self.llm
        research_agent = self._create_agent(llm, [tavily_tool], "You are a web researcher.")
        research_node = functools.partial(self._agent_node, agent=research_agent, name="Researcher")
        return research_node