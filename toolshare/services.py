# toolshare/services.py

from toolshare.db import SessionLocal, User, Tool

# Create a new user
def create_user(username, email):
    session = SessionLocal()
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user

# List all users
def list_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users

# Create a new tool
def create_tool(name, description, owner_id):
    session = SessionLocal()
    tool = Tool(name=name, description=description, owner_id=owner_id)
    session.add(tool)
    session.commit()
    session.refresh(tool)
    session.close()
    return tool

# List all tools
def list_tools():
    session = SessionLocal()
    tools = session.query(Tool).all()
    session.close()
    return tools
