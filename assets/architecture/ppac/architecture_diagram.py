from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.database import Mongodb
from diagrams.aws.storage import S3
from diagrams.firebase.base import Firebase
from diagrams.programming.language import Nodejs
from diagrams.generic.device import Mobile

with Diagram("Farmeme Modern CI/CD & Architecture", show=False, direction="LR"):
    # Client
    client = Mobile("Mobile Client")

    # Source Control
    source = Github("GitHub Repo")

    with Cluster("CI/CD Pipeline"):
        ci = GithubActions("GitHub Actions")
        build = Nodejs("Build & Test")
        source >> ci >> build

    with Cluster("Production Environment"):
        with Cluster("Backend App"):
            server = Nodejs("Express API Server")
            
            with Cluster("Internal Layers"):
                controllers = Nodejs("Controllers")
                services = Nodejs("Services")
                models = Nodejs("Models")
                controllers >> services >> models
            
            with Cluster("Middleware / Utils"):
                compression = Nodejs("Image Compression\n(Sharp/HEIC)")

            server >> controllers
            server >> compression

        db = Mongodb("MongoDB Atlas")
        s3 = S3("AWS S3 (Memes)")
        fcm = Firebase("Firebase (FCM)")

        models >> db
        compression >> Edge(label="upload compressed") >> s3
        services >> s3
        services >> fcm

    # Pipeline Flow
    build >> Edge(color="darkgreen", label="deploy") >> server
    client >> Edge(label="Upload Image / API") >> server
