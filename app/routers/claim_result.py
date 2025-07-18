from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.claim_result import ClaimResult
from app.schemas.claim_result import ClaimResultIn, ClaimResultOut
from app.dependencies import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Get All Claims by user_id
@router.get("/user/{user_id}", response_model=List[ClaimResultOut])
async def get_claims_by_user(user_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(ClaimResult).where(ClaimResult.user_id == user_id)
    result = await db.execute(stmt)
    claims = result.scalars().all()

    if not claims:
        raise HTTPException(status_code=404, detail="No claims found for this user")

    return claims


@router.post("/save", response_model=ClaimResultOut)
async def store_claim_result(payload: ClaimResultIn, db: AsyncSession = Depends(get_db)):
    # Check for existing claim
    stmt = select(ClaimResult).where(ClaimResult.claim_id == payload.claim_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Claim with this ID already exists")

    # Create new claim result
    new_result = ClaimResult(
        claim_id=payload.claim_id,
        claim=payload.claim,
        verdict_data=payload.verdict_data,
        user_id=payload.user_id
    )

    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)

    return new_result


@router.get("/{claim_id}", response_model=ClaimResultOut)
async def get_claim_result(claim_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(ClaimResult).where(ClaimResult.claim_id == claim_id)
    result = await db.execute(stmt)
    claim = result.scalar_one_or_none()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim


@router.get("/{claim_id}/verdict")
async def get_verdict_data(claim_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(ClaimResult).where(ClaimResult.claim_id == claim_id)
    result = await db.execute(stmt)
    claim = result.scalar_one_or_none()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim.verdict_data  # return only the JSON object

# @router.post("/save", response_model=ClaimResultOut)
# def store_claim_result(payload: ClaimResultIn, db: Session = Depends(get_db)):
#     existing = db.query(ClaimResult).filter_by(claim_id=payload.claim_id).first()
#     if existing:
#         raise HTTPException(status_code=409, detail="Claim with this ID already exists")

#     result = ClaimResult(
#         claim_id=payload.claim_id,
#         claim=payload.claim,
#         verdict_data=payload.verdict_data,
#         user_id=payload.user_id  # associate claim with user
#     )

#     db.add(result)
#     db.commit()
#     db.refresh(result)

#     return result


# @router.get("/{claim_id}", response_model=ClaimResultOut)
# def get_claim_result(claim_id: str, db: Session = Depends(get_db)):
#     result = db.query(ClaimResult).filter_by(claim_id=claim_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Claim not found")

#     return result

# @router.get("/{claim_id}/verdict")
# def get_verdict_data(claim_id: str, db: Session = Depends(get_db)):
#     result = db.query(ClaimResult).filter_by(claim_id=claim_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Claim not found")

#     return result.verdict_data  # this returns only the JSON object