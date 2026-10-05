import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueUpdate, IssueOutput
from app.storage import load_issues, save_issues

router = APIRouter(
    prefix="/issues",
    tags=["issues"],
)

issues = load_issues()

@router.get("/", response_model=list[IssueOutput])
async def get_issues():
    return issues

@router.post("/", response_model=IssueOutput, status_code=status.HTTP_201_CREATED)
async def create_issue(issue: IssueCreate):
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": issue.title,
        "description": issue.description,
        "status": issue.status,
        "priority": issue.priority,
    }
    issues.append(new_issue)
    save_issues(issues)
    return new_issue

@router.get("/{issue_id}", response_model=IssueOutput)
async def get_issue(issue_id: str):
    for issue in issues:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{issue_id}", response_model=IssueOutput)
async def update_issue(issue_id: str, issue_update: IssueUpdate):
    for issue in issues:
        if issue["id"] == issue_id:
            if issue_update.title is not None:
                issue["title"] = issue_update.title
            if issue_update.description is not None:
                issue["description"] = issue_update.description
            if issue_update.status is not None:
                issue["status"] = issue_update.status
            if issue_update.priority is not None:
                issue["priority"] = issue_update.priority
            save_issues(issues)
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(issue_id: str):
    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:
            del issues[index]
            save_issues(issues)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
