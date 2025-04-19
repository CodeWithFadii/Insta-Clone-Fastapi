from typing import List, Optional
from uuid import UUID
from fastapi import Depends, File, HTTPException, UploadFile, status, APIRouter
from sqlalchemy.orm import Session
import fitz
from app import models, oauth2, schemas, utils
from app.database import get_db

router = APIRouter(tags=["Users"])


# Getting a user by Token
@router.get("/user", response_model=schemas.UserOut)
def get_current_user(
    user_data: schemas.User = Depends(oauth2.get_current_user),
):
    try:
        return schemas.UserOut(user=user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.post("/read-pdf", response_model=List[schemas.ExtractionResult])
async def read_pdf(files: List[UploadFile] = File(...)):
    # Check if any files were uploaded
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    results = []
    for file in files:
        # Validate that the file is a PDF
        if file.content_type != "application/pdf":
            results.append(
                schemas.ExtractionResult(filename=file.filename, error="Not a PDF file.")  # type: ignore
            )
            continue

        try:
            # Read the file contents asynchronously
            contents = await file.read()

            # Load the PDF from bytes
            pdf = fitz.open(stream=contents, filetype="pdf")

            # Extract text from all pages
            text = ""
            for page in pdf:
                text += page.get_text()  # type: ignore

            # Clean the extracted text
            cleaned_text = text.strip()

            # Close the PDF to free resources
            pdf.close()

            # Add successful extraction to results
            results.append(schemas.ExtractionResult(filename=file.filename, text=cleaned_text))  # type: ignore

        except Exception as e:
            # Add error information if processing fails
            results.append(
                schemas.ExtractionResult(filename=file.filename, error=str(e))  # type: ignore
            )

    return results


# Getting a user by ID
@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
):
    try:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no user with id: {id}",
            )

        return schemas.UserOut(user=schemas.User.model_validate(user))

    except HTTPException as e:
        raise e  # Reraise the HTTPException for custom error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the user: {str(e)}",
        )


# Getting all users
@router.get("/users", response_model=schemas.PaginatedUsers)
def get_users_with_cursor(
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
    limit: int = 10,  # Default to 10 users per page
    cursor: Optional[UUID] = None,  # Cursor to indicate where to start fetching users
):
    try:
        if limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit exceeds the maximum allowed value of 100.",
            )

        # Get the total number of users
        total_users = db.query(models.User).count()

        # Query for users starting from the given cursor (if any)
        query = db.query(models.User).order_by(models.User.id)

        if cursor:
            query = query.filter(models.User.id > cursor)

        users_query = query.limit(limit).all()

        if not users_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found.",
            )

        users_list = [schemas.User.model_validate(user) for user in users_query]

        # Get the id of the last user to be used as the cursor for the next request
        next_cursor = users_query[-1].id if users_query else None
        # Correctly assign the id value

        return schemas.PaginatedUsers(
            users=users_list, total_count=total_users, next_cursor=next_cursor  # type: ignore
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching users: {str(e)}",
        )
