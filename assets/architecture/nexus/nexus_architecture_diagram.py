from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.programming.language import Nodejs, TypeScript
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.custom import Custom

# --- Diagram Configuration ---
graph_attr = {
    "fontsize": "20",
    "bgcolor": "white"
}

with Diagram("Arkain Nexus (AI Console MCP) Architecture", 
             filename="nexus_architecture_flow", 
             show=False, 
             direction="LR", 
             graph_attr=graph_attr):
    
    user = Users("User")

    with Cluster("Arkain Ecosystem"):
        ide_site = TypeScript("ide-site\n(Frontend / Chat UI)")
        
        with Cluster("MCP Layer"):
            mcp_client = Nodejs("MCP-Client\n(Tool Dispatcher)")
            mcp_server = Nodejs("nexus-console-server\n(MCP-Server / Tools)")

        llm_api = Nodejs("LLM-API-Server\n(Prompting & Filter)")

    with Cluster("External Services"):
        llm_provider = Internet("LLM Provider\n(Claude / OpenAI)")
        gitbook_ai = Internet("GitBook AI\n(Docs RAG)")

    # --- Communication Flow ---

    # 1. User Interaction
    user >> Edge(label="Query", color="darkblue") >> ide_site

    # 2. MCP Initialization & Tool Execution
    ide_site >> Edge(label="1. Request Tool", color="orange") >> mcp_client
    mcp_client >> Edge(label="2. Call Tool", color="orange") >> mcp_server
    
    # 3. Data Fetching (Server to IDE)
    mcp_server >> Edge(label="3. Fetch Data\n(Credit/Container)", style="dashed", color="darkgreen") >> ide_site
    
    # 4. LLM Processing
    mcp_client >> Edge(label="4. 1st Response", color="brown") >> llm_api
    llm_api >> Edge(label="5. Final Prompt", color="purple") >> llm_provider
    
    # 5. External RAG
    mcp_server >> Edge(label="Search Docs", color="darkgreen") >> gitbook_ai

    # 6. Final Response to User
    llm_api >> Edge(label="6. Styled Response", color="darkblue") >> ide_site
    ide_site >> Edge(label="UI Update / Action", color="darkblue") >> user
