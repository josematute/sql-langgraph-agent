"""Configuration management for database connection and model provider."""

import os
import sys

import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_community.utilities import SQLDatabase
from sqlalchemy.exc import ProgrammingError, OperationalError

# Load environment variables from .env
load_dotenv()

# Default local PostgreSQL database (Docker container)
DEFAULT_POSTGRES_URI = (
    "postgresql://postgres:postgres@localhost:5432/sample_db"
)


def get_database_uri() -> str:
    """
    Get PostgreSQL URI with fallback to default.

    Priority:
    1. POSTGRES_URI env var (if provided)
    2. Default public PostgreSQL database
    """
    uri = os.getenv("POSTGRES_URI")
    if uri:
        return uri
    return DEFAULT_POSTGRES_URI


def get_database() -> SQLDatabase:
    """
    Get SQLDatabase instance for PostgreSQL.
    
    Raises:
        SystemExit: If database connection fails with a user-friendly error message.
    """
    uri = get_database_uri()
    
    try:
        # Try to create database connection with schema reflection
        # Some databases may have limited permissions, so we'll handle that gracefully
        return SQLDatabase.from_uri(uri)
    except (ProgrammingError, OperationalError) as e:
        # Connection or permission error
        error_msg = str(e)
        
        # Provide user-friendly error message
        print("\n" + "=" * 60, file=sys.stderr)
        print("❌ Database Connection Error", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("\nThere was a problem connecting to the PostgreSQL database.", file=sys.stderr)
        print("\nPossible causes:", file=sys.stderr)
        print("  • Database server is not accessible", file=sys.stderr)
        print("  • Insufficient permissions for schema reflection", file=sys.stderr)
        print("  • Invalid connection string", file=sys.stderr)
        print("\nTo fix:", file=sys.stderr)
        print("  1. Start the default database: docker-compose up -d", file=sys.stderr)
        print("  2. Or set POSTGRES_URI in your .env file with your own database", file=sys.stderr)
        print(f"\nConnection URI: {uri.split('@')[1] if '@' in uri else 'hidden'}", file=sys.stderr)
        print(f"\nTechnical error: {error_msg[:200]}...", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Other unexpected errors
        print("\n" + "=" * 60, file=sys.stderr)
        print("❌ Unexpected Database Error", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"\nAn unexpected error occurred while connecting to the database:", file=sys.stderr)
        print(f"{type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
        print("\nPlease check your database connection settings.", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)


# Default model configurations
DEFAULT_OPENAI_MODEL = "openai:gpt-4o-mini"
DEFAULT_BEDROCK_MODEL = "anthropic.claude-haiku-4-5-20251001-v1:0"
DEFAULT_AWS_REGION = "us-east-1"


def _get_aws_credentials():
    """
    Get AWS credentials from environment variables.
    
    Returns:
        tuple: (credentials_dict, session_or_none, should_use_profile)
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")
    aws_profile = os.getenv("AWS_PROFILE")
    
    # Check for AWS profile configuration
    if aws_profile:
        session = boto3.Session(profile_name=aws_profile)
        return {}, session, True
    
    # Use direct credentials
    credentials = {}
    if aws_access_key_id:
        credentials["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        credentials["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        credentials["aws_session_token"] = aws_session_token
    
    return credentials, None, False


def get_model():
    """
    Get the model to use for the agent.
    
    Priority:
    1. MODEL_PROVIDER env var (if set to "bedrock" or "openai")
    2. If AWS credentials exist and MODEL_PROVIDER not set → use Bedrock
    3. Default to OpenAI
    
    Returns:
        Model instance (ChatBedrockConverse) or model string (for OpenAI)
    """
    model_provider = os.getenv("MODEL_PROVIDER", "").lower()
    
    # Explicit provider selection
    if model_provider == "bedrock":
        return _create_bedrock_model()
    elif model_provider == "openai":
        return DEFAULT_OPENAI_MODEL
    
    # Auto-detect: check if AWS credentials are available
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_profile = os.getenv("AWS_PROFILE")
    
    if (aws_access_key and aws_secret_key) or aws_profile:
        # AWS credentials found, use Bedrock
        return _create_bedrock_model()
    
    # Default to OpenAI
    return DEFAULT_OPENAI_MODEL


def _create_bedrock_model():
    """
    Create and return a ChatBedrockConverse model instance.
    
    Returns:
        ChatBedrockConverse instance
    
    Raises:
        ValueError: If AWS credentials are not properly configured
    """
    credentials, session, use_profile = _get_aws_credentials()
    region = os.getenv("AWS_REGION", DEFAULT_AWS_REGION)
    model_id = os.getenv("BEDROCK_MODEL_ID", DEFAULT_BEDROCK_MODEL)
    
    if use_profile:
        # Using AWS profile
        return ChatBedrockConverse(
            model=model_id,
            region_name=region,
            client=session.client("bedrock-runtime", region_name=region),
        )
    else:
        # Using direct credentials
        # If no credentials provided, boto3 will use default credential chain (IAM role, environment, etc.)
        if credentials:
            return ChatBedrockConverse(
                model=model_id,
                region_name=region,
                **credentials,
            )
        else:
            # No explicit credentials, let boto3 use default credential chain
            return ChatBedrockConverse(
                model=model_id,
                region_name=region,
            )
