#!/usr/bin/env python3
"""
Orchestration & Manual Trigger (Component E)
CLI script to run the end-to-end ingestion process for user profiles.

Usage:
    python repo_src/scripts/ingest_user.py <filepath>
    OR via pnpm: pnpm run ingest-user <filepath>
"""
import sys
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from repo_src.backend.pipelines.user_ingestion import process_file_sync
from repo_src.backend.functions.users import create_or_update_user
from repo_src.backend.database.connection import SessionLocal, engine
from repo_src.backend.database.models import Base
from repo_src.backend.data.schemas import UserCreate


def ensure_database():
    """Ensure the database tables exist"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables verified/created")


def ingest_user_from_file(file_path: str) -> dict:
    """
    Main ingestion function: processes a file and saves to database.

    Args:
        file_path: Path to the file to ingest

    Returns:
        Dictionary with status and user data
    """
    print(f"\n{'='*60}")
    print(f"STARTING USER INGESTION")
    print(f"{'='*60}\n")

    # Step 1: Ensure database is ready
    print("Step 1: Ensuring database is ready...")
    ensure_database()

    # Step 2: Process the file with LLM
    print(f"\nStep 2: Processing file: {file_path}")
    print("   This will use the LLM to extract user profile data...")

    try:
        user_data_dict = process_file_sync(file_path)
        print(f"✓ Successfully extracted user data for: {user_data_dict.get('name', 'Unknown')}")
        print(f"   User ID: {user_data_dict.get('user_id', 'Unknown')}")
        print(f"   Bio: {user_data_dict.get('bio', 'N/A')[:80]}...")
    except Exception as e:
        print(f"✗ Error processing file: {e}")
        return {"status": "error", "message": str(e)}

    # Step 3: Save to database
    print("\nStep 3: Saving user profile to database...")
    db = SessionLocal()
    try:
        user_create = UserCreate(**user_data_dict)
        db_user = create_or_update_user(db, user_create)

        print(f"✓ Successfully saved/updated user: {db_user.name}")
        print(f"   Database ID: {db_user.id}")
        print(f"   User ID: {db_user.user_id}")
        print(f"   Created: {db_user.created_at}")
        print(f"   Updated: {db_user.updated_at}")

        result = {
            "status": "success",
            "user_id": db_user.user_id,
            "name": db_user.name,
            "database_id": db_user.id
        }

    except Exception as e:
        print(f"✗ Error saving to database: {e}")
        result = {"status": "error", "message": str(e)}
    finally:
        db.close()

    print(f"\n{'='*60}")
    print(f"INGESTION COMPLETE")
    print(f"{'='*60}\n")

    return result


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Ingest a user profile from a text file into the Social OS database"
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the text file containing user profile information"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Verify file exists
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File not found: {args.file_path}")
        sys.exit(1)

    # Run ingestion
    result = ingest_user_from_file(str(file_path.absolute()))

    # Exit with appropriate code
    if result["status"] == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
