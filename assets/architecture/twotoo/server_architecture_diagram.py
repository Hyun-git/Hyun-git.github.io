from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.programming.language import Nodejs
from diagrams.onprem.database import Mongodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.onprem.compute import Server
from diagrams.aws.compute import Lambda

# --- 아이콘 설정 (최적의 조합) ---
try:
    from diagrams.onprem.network import Internet as Express 
except ImportError:
    from diagrams.programming.language import Nodejs as Express

try:
    from diagrams.aws.engagement import SimpleNotificationService as Firebase
except ImportError:
    from diagrams.onprem.compute import Server as Firebase

try:
    from diagrams.onprem.monitoring import Prometheus as PM2
except ImportError:
    from diagrams.onprem.compute import Server as PM2

try:
    from diagrams.aws.management import Cloudwatch as Cron
except ImportError:
    from diagrams.onprem.compute import Server as Cron

# --- 다이어그램 생성 ---
graph_attr = {
    "fontsize": "20",
    "bgcolor": "white"
}

with Diagram("TwoToo Server Full Architecture", filename="twotoo_full_architecture", show=False, direction="LR", graph_attr=graph_attr):
    
    client = Users("App Clients\n(iOS/Android)")
    main_db = Mongodb("MongoDB Cluster\n(Challenge/Commit/User)")

    # 1. 메인 백엔드 (EC2)
    with Cluster("AWS EC2 Instance (Ubuntu)"):
        api_gateway = Express("Express API")
        
        with Cluster("Log Management"):
            log_manager = PM2("PM2-Logrotate")
            log_cron = Cron("Log Cron Job\n(00:05 UTC)")
            local_logs = Server("Local Logs\n(/pm2/logs)")
            
            api_gateway >> Edge(label="write", style="dotted") >> local_logs
            log_manager >> Edge(label="manage") >> local_logs
            log_cron >> Edge(label="sync & delete", color="red") >> local_logs

        with Cluster("Application Layers"):
            services = Nodejs("Business Logic")
            db_models = Mongodb("Mongoose")
            
            api_gateway >> services >> db_models

    # 2. 서버리스 알림 시스템 (Lambda)
    with Cluster("Scheduled Notifications"):
        noti_lambda = Lambda("Commit Remind\nLambda")
        trigger = Eventbridge("EventBridge\n(Scheduler)")
        
        # 람다 로직 흐름
        trigger >> Edge(label="Invoke", color="brown") >> noti_lambda
        noti_lambda >> Edge(label="Aggregate Query", color="darkgreen", style="dashed") >> main_db

    # 3. 클라우드 서비스
    with Cluster("Cloud Services"):
        s3_images = S3("S3: Images")
        s3_logs = S3("S3: Server Logs\n(Backup)")
        push_service = Firebase("FCM\n(Push Notification)")

    # --- 전체 연결 관계 ---
    
    # Client Access
    client >> Edge(label="REST API", color="darkblue") >> api_gateway
    push_service >> Edge(label="Push Alert", color="purple", style="dashed") >> client

    # Data Flow
    db_models >> main_db
    services >> Edge(color="orange", style="dashed") >> s3_images
    log_cron >> Edge(label="AWS CLI Sync", color="blue") >> s3_logs
    
    # Lambda Integration
    noti_lambda >> Edge(label="Send Push", color="purple") >> push_service
