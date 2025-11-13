#!/usr/bin/env python3
"""
Seed the database with test user data for development and testing.
This bypasses the LLM ingestion and directly inserts sample users.

Usage:
    python repo_src/scripts/seed_test_users.py
    OR via pnpm: pnpm run seed-users
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from repo_src.backend.functions.users import create_or_update_user
from repo_src.backend.database.connection import SessionLocal, engine
from repo_src.backend.database.models import Base
from repo_src.backend.data.schemas import UserCreate


# Sample user data
SAMPLE_USERS = [
    {
        "user_id": "alice_johnson",
        "name": "Alice Johnson",
        "bio": "Software engineer and cloud architecture specialist",
        "wiki_content": """## Background

Alice Johnson is a software engineer with 8 years of experience in the tech industry. She holds a degree in Computer Science from MIT and has built a strong reputation in distributed systems and cloud architecture.

## Professional Experience

- **Early Career**: Started at a fintech startup building microservices for payment processing
  - Handled millions of transactions per day
  - Learned about reliability and fault tolerance
- **Mid Career**: Led development of a real-time analytics platform
  - Technologies: Kafka, Apache Spark, Kubernetes
- **Current**: Cloud architecture consultant
  - Focus on AWS and GCP migrations
  - Specializes in serverless architectures and cost optimization

## Technical Skills

### Programming Languages
- **Python**: Data processing and machine learning pipelines
- **Go**: High-performance backend services
- **TypeScript/Node.js**: Full-stack development

### Infrastructure & DevOps
- AWS Certified
- Docker & Kubernetes expert
- Terraform
- CI/CD pipelines

## Interests & Activities

### Open Source
- Maintains several Python libraries
- Active contributor to major open source projects
- Passionate about giving back to the community

### Mentorship
- Volunteers with Code2040
- Helps underrepresented minorities break into tech
- Regular speaker at tech meetups

### Rock Climbing
- Avid outdoor climber
- Climbed in Yosemite, Red Rocks, and the Dolomites
- Finds parallels between climbing and problem-solving in tech

### Other Hobbies
- Science fiction reader
- Strategy board game enthusiast
- Weekly game night organizer

## Career Goals

- Interested in the intersection of infrastructure and machine learning
- Exploring MLOps and ML platform engineering
- Considering starting own company focused on developer tools
- Strong advocate for work-life balance and mental health in tech
"""
    },
    {
        "user_id": "bob_chen",
        "name": "Robert Chen",
        "bio": "Senior Product Designer and design systems expert",
        "wiki_content": """## About

Robert "Bob" Chen is a Senior Product Designer with 6 years of experience in the tech industry. He graduated from Rhode Island School of Design (RISD) with a degree in Industrial Design and successfully transitioned to digital product design.

## Career Journey

### Early Career
- Started in mobile gaming company
- Learned fundamentals of UX/UI design
- Fell in love with iterative design and user testing

### Growth Phase
- First designer at a B2B SaaS company
- Wore many hats: user research, visual design, prototyping, front-end dev
- Built design culture from scratch

### Current Role (TechFlow Inc.)
- Senior Product Designer
- Leads design for project management tool used by 100,000+ teams
- Built comprehensive design system from scratch
- Known for collaborative and pragmatic approach

## Skills & Expertise

### Design Tools
- Expert in Figma, Sketch, Adobe Creative Suite
- Advanced prototyping (Framer, Principle, After Effects)

### Research & Process
- User research methodologies
- Usability testing and interviews
- Design sprints and workshop facilitation

### Technical Skills
- Front-end coding: HTML, CSS, React
- Design systems and component libraries
- Accessibility (WCAG standards)

## Design Philosophy

- "Good design is invisible"
- Influenced by Don Norman and Dieter Rams
- Strong believer in human-centered design
- Passionate about accessibility and inclusive design

## Beyond Design

### Photography
- Amateur street photographer
- Work exhibited in local galleries
- Photography informs his design sensibility
- Strong eye for composition, color, and light

### Cooking
- Passionate home cook
- Experimenting with Thai, Vietnamese, and Japanese cuisines
- Finds parallels between cooking and design process

### Learning
- Avid podcast listener
- Favorites: 99% Invisible, Design Matters, The Tim Ferriss Show

## Community Involvement

- Mentors junior designers through ADPList
- Regular speaker at design meetups
- Published articles on Medium about design process and career advice
- Active in design community

## Future Aspirations

- Transition into design leadership
- More writing and content creation
- Possibly start YouTube channel
- Long-term: teach design at university level part-time
"""
    },
    {
        "user_id": "carol_martinez",
        "name": "Dr. Carol Martinez",
        "bio": "Computational biologist specializing in genomics and AI",
        "wiki_content": """## Academic Background

Dr. Carol Martinez holds a PhD in Bioinformatics from Stanford University, where her dissertation focused on developing machine learning algorithms to predict protein structures from genomic sequences.

## Professional Experience

### Postdoctoral Research (UCSF)
- Worked on cancer genomics
- Developed computational pipelines for tumor DNA analysis
- Identified potential drug targets
- Published in Nature and Cell

### Current Position (BioGenix)
- Principal Scientist
- Leads computational infrastructure for genomic analysis
- Processes thousands of whole genome sequences
- Uses AI to identify genetic variants and drug responses

## Technical Expertise

### Programming & Tools
- Expert in Python, R, and Julia for scientific computing
- Bioinformatics tools: BWA, GATK, SAMtools
- Machine learning: scikit-learn, TensorFlow, PyTorch

### Infrastructure
- High-performance computing
- Cloud platforms: AWS, Google Cloud
- Database management: SQL, NoSQL, graph databases

### Domain Knowledge
- Next-generation sequencing data analysis
- Statistical analysis and experimental design
- Multi-omics data integration

## Research Interests

### Current Focus
- Deep learning applications in biology
- Multi-omics integration (genomics, transcriptomics, proteomics, metabolomics)
- AI in drug discovery
- Personalized medicine

### Vision
Believes we're in a golden age where large biological datasets combined with powerful ML models will lead to breakthrough discoveries in disease understanding and treatment development.

## Academic Engagement

### Teaching
- Adjunct Professor at UC Berkeley
- Teaches graduate course on computational genomics
- Passionate about education and staying connected to research

### Mentorship
- Focuses on increasing diversity in STEM
- Mentors underrepresented students
- Helps with graduate school applications and career guidance

## Personal Interests

### Ultramarathon Running
- Completed several 50-mile races
- Training for first 100-miler
- Draws parallels between ultra running mental toughness and research persistence

### Science Communication
- Writes blog explaining complex biology in accessible language
- Discusses ethics of genomics and personalized medicine
- TEDx speaker
- Podcast guest on future of healthcare

### Languages & Global Impact
- Fluent in English, Spanish, and Portuguese
- Supports science education in Latin America
- Organized workshops in Mexico, Brazil, and Colombia

## Vision & Goals

### Long-term Vision
- Computational biology as standard part of medical practice
- Every patient with genome sequenced
- AI-assisted personalized treatment decisions

### Ethical Considerations
- Ensuring equitable access to genomic medicine
- Protecting genetic privacy
- Preventing genetic discrimination
- Scientists' responsibility in shaping policy

### Career Trajectory
- Transition to more strategic role
- Possibly Chief Scientific Officer
- Or founding own biotech company focused on AI-driven drug discovery
"""
    }
]


def ensure_database():
    """Ensure the database tables exist"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables verified/created")


def seed_users():
    """Seed the database with sample users"""
    print(f"\n{'='*60}")
    print(f"SEEDING DATABASE WITH TEST USERS")
    print(f"{'='*60}\n")

    # Ensure database is ready
    print("Step 1: Ensuring database is ready...")
    ensure_database()

    # Create session
    db = SessionLocal()
    success_count = 0
    error_count = 0

    try:
        print(f"\nStep 2: Creating/updating {len(SAMPLE_USERS)} users...\n")

        for user_data in SAMPLE_USERS:
            try:
                user_create = UserCreate(**user_data)
                db_user = create_or_update_user(db, user_create)

                print(f"✓ {db_user.name} (@{db_user.user_id})")
                print(f"   ID: {db_user.id} | Created: {db_user.created_at}")
                success_count += 1

            except Exception as e:
                print(f"✗ Error creating user {user_data['name']}: {e}")
                error_count += 1

    finally:
        db.close()

    print(f"\n{'='*60}")
    print(f"SEEDING COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully created/updated: {success_count} users")
    if error_count > 0:
        print(f"Errors: {error_count}")
    print()

    return success_count > 0


if __name__ == "__main__":
    success = seed_users()
    sys.exit(0 if success else 1)
