from langchain_openai import ChatOpenAI
from .nodes import Nodes
from .state import AgentState
from langgraph.graph import StateGraph, END

from dotenv import load_dotenv
load_dotenv()



class WorkFlow():
	llm: ChatOpenAI
    
	def __init__(self, llm=None):
		llm = llm or ChatOpenAI(model="gpt-4-1106-preview")
		# llm=ChatOpenAI(model="gpt-3.5-turbo")
		
		nodes = Nodes(llm=llm)
		workflow = StateGraph(AgentState)
		

		workflow.add_node("Researcher", nodes.research_node(llm=ChatOpenAI(model="gpt-3.5-turbo")))
		workflow.add_node("Coder", nodes.code_node())
		workflow.add_node("supervisor", nodes.supervisor_chain_node())
		
        # add edges
		# We want our workers to ALWAYS "report back" to the supervisor when done
		workflow.add_edge("Researcher", "supervisor")
		workflow.add_edge("Coder", "supervisor")
		
		conditional_map = {
			'Researcher': 'Researcher', 
			'Coder': 'Coder',
			'FINISH': END,
		}
		
		workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
		
        # Finally, add entrypoint
		workflow.set_entry_point("supervisor")
  
		self.graph = workflow.compile()