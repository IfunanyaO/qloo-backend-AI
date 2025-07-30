from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.UserHistory import UserHistory
from app.models.student import Student
from app.schemas.student import StudentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = APIRouter()

@router.post("/save")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")

    new_student = Student(name=student.name, email=student.email, major=student.major)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "id": new_student.id,
        "name": new_student.name,
        "email": new_student.email,
        "major": new_student.major
    }

@router.get("/all")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "major": s.major
        }
        for s in students
    ]


@router.post("/test")
async def save_test_history(db: AsyncSession = Depends(get_db)):
    test_history = UserHistory(
        id=uuid4(),
        user_id="dbea7932-f80d-49d5-a915-0fa2ca7df43b",
        prompt="I’m planning a 5-day trip to New york. I’m into jazz music, seafood, and browsing indie bookstores. I want something relaxing and low budget.",
        destination="Libson",
        duration="5 days",
        tastes="tea, shrines, nature",
        style="cozy, peaceful",
        generated_itinerary="""## Day 1 (September 1st, 2025)\n\n#### Morning\nBegin your Lisbon adventure at the **Note! Ferreira Borges**. This cozy stationery shop also sells a variety of magazines and has a quaint indie ambience. Ideal for those who love to browse bookstores. \n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Note!+Ferreira+Borges+Lisbon)  \n🌐 http://www.noteonline.pt/  \n⭐ Rating: 4.3  \n\n#### Afternoon \nNext, enjoy lunch at the **Solar dos Presuntos**, a delightful eatery known for its delicious Portuguese food, especially seafood. Don't forget to try the octopus!\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Solar+dos+Presuntos+Lisbon)  \n📞 +351213424253  \n🌐 http://www.solardospresuntos.com/  \n⭐ Rating: 4.5  \n\n#### Evening \nEnd your day with a relaxing night of live jazz music at **Spicy cafe** which also serves delightful tartines. Let the rhythmic melodies carry you into the Portuguese nightlife. \n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Spicy+cafe+Lisbon)  \n📞 +351218246561  \n🌐 http://spicycafe.eatbu.com/  \n⭐ Rating: 4.2  \n\nWeather: Clear Sky, 28.4°C - a casual, airy outfit would be suitable.\n\n## Day 2 (September 2nd, 2025)\n\n#### Morning  \nStart your day with a trip to **Tinta nos Nervos**. This unique bookstore specializes in art space, and illustrative masterpieces - a paradise for indie bookstore enthusiasts.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Tinta+nos+Nervos+Lisbon)  \n📞 +351213951179  \n🌐 http://tintanosnervos.com/  \n⭐ Rating: 4.9\n\n#### Afternoon \nTreat your taste buds to a budget-friendly lunch at **Mineiro da Brandoa**. The restaurant offers a variety of buffet options for a great price.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Mineiro+da+Brandoa+Lisbon)  \n📞 +351962717643  \n🌐 http://mineiro.com.pt/brandoa  \n⭐ Rating: 4.1  \n\n#### Evening  \nUnwind with dinner at the **Brasuca**. Known for its feijoada and moqueca, this spot is a haven for seafood.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Brasuca+Lisbon)  \n📞 +351213220740  \n🌐 http://www.restaurantebrasuca.com/  \n⭐ Rating: 4.5\n\nWeather: Clear Sky, 28.76°C - don't forget sunscreen and a hat.\n\n## Day 3 (September 3rd, 2025)\n\n#### Morning  \nGrab a book and chill at **Starbucks**. They also offer a nice selection of cakes in a comfortable environment which makes the price totally worth it. \n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Starbucks+Lisbon)  \n📞 +351932908856  \n🌐 http://www.starbucks.pt/  \n⭐ Rating: 4.1  \n\n#### Afternoon \nSomething unique on the menu for lunch: **O Velho Farelo**, known for its grilled meals including the delicious seafood espetada. \n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=O+Velho+Farelo+Lisbon)  \n📞 +351211531455  \n🌐 https://www.facebook.com/velhofarelo/  \n⭐ Rating: 4.1 \n\n#### Evening  \nMingle with the locals on a relaxed evening at **Alfama Rio**. This spot is a hit among locals and tourists for its burgers, prices, and sangria! \n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Alfama+Rio+Lisbon)  \n📞 +351919094169  \n🌐 https://www.facebook.com/21Alfama.Rio/  \n⭐ Rating: 4.6\n\nWeather: Clear Sky, 28.08°C - stay cool and hydrated.\n\n## Day 4 (September 4th, 2025)\n\n#### Morning  \nBegin the day with a delicious breakfast at **A Padaria Portuguesa**. Known for its flavorful croissants, this place offers great food at great prices.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=A+Padaria+Portuguesa+Lisbon)  \n📞 +351926963656  \n🌐 http://www.apadariaportuguesa.pt/  \n⭐ Rating: 3.8\n\n#### Afternoon  \nFor lunch, try the buffet at **Sihai**. The price is friendly, and the crepes are to die for.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Sihai+Lisbon)  \n📞 +351217609943  \n⭐ Rating: 4  \n\n#### Evening  \nIndulge in the lively vibes of **Hamburgueria do Bairro (São Bento)** for dinner. They also have tantalizing vegan options, and their prices are great for a budget-friendly trip.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Hamburgueria+do+Bairro+(São+Bento)+Lisbon)  \n📞 +351213960405   \n🌐 http://www.hamburgueriadobairro.pt/  \n⭐ Rating: 4.1  \n\nWeather: Clear Sky, 25.95°C - layer your outfit for a cooler evening.\n\n## Day 5 (September 5th, 2025)\n\n#### Morning  \nSqueeze in one more indie bookshop visit to **World Academy**. This short course institute also houses an amazing collection of interesting books.\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=World+Academy+Lisbon)  \n📞 +351218210366  \n🌐 http://www.worldacademy.pt/  \n⭐ Rating: 4.3\n\n#### Afternoon  \nA trip to Lisbon would be incomplete without visiting **Sabores da Ilha**. Positioned near a shopping center, this place offers tasty wood-fired espetada!\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Sabores+da+Ilha+Lisbon)  \n📞 +351214072176  \n🌐 https://www.tripadvisor.pt/Restaurant_Review-g2218978-d13350741-Reviews-Sabores_Da_Ilha-Carnaxide_Lisbon_District_Central_Portugal.html  \n⭐ Rating: 3.6\n\n#### Evening  \nEnd your Lisbon tour with a sweet stop at **Leonidas Campo de Ourique**. This spot is famous for its delicious jams!\n\n📍 [Map it](https://www.google.com/maps/search/?api=1&query=Leonidas+Campo+de+Ourique+Lisbon)  \n📞 +351214074023  \n🌐 https://www.facebook.com/leonidaschocolateecafe  \n⭐ Rating: 4.9  \n\nWeather: Clear Sky, 29.09°C - keep it summer-casual, with a light top and shorts.\n\n# Recap: \"A melody of savory seafood, soulful jazz, and indie bookstores veiled in Lisbon’s allure. A budget-friendly retreat into relaxation. 5 days in Lisbon, a rhythm echoing through time!\" 🎷📖🦐\n
"""
    )
    db.add(test_history)
    await db.commit()
    return {"message": "Test user history with JSON itinerary saved!"}



async def save_user_itinerary(
    db: AsyncSession,
    user_id: str,
    prompt: str,
    destination: str,
    duration: str,
    tastes: str,
    style: str,
    generated_itinerary: dict
):
    itinerary = UserHistory(
        id=uuid4(),
        user_id=user_id,
        prompt=prompt,
        destination=destination,
        duration=duration,
        tastes=tastes,
        style=style,
        generated_itinerary=generated_itinerary
    )
    db.add(itinerary)
    await db.commit()
    await db.refresh(itinerary)  # Optional: to return the saved object with DB-generated fields
    return {"message": "User itinerary saved!", "id": str(itinerary.id)}


@router.get("/history")
async def get_all_user_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserHistory))
    histories = result.scalars().all()

    return [
        {
            "id": str(history.id),
            "user_id": str(history.user_id),
            "prompt": history.prompt,
            "destination": history.destination,
            "duration": history.duration,
            "tastes": history.tastes,
            "style": history.style,
            "generated_itinerary": history.generated_itinerary,  # already JSON
            "created_at": history.created_at.isoformat(),
            "updated_at": history.updated_at.isoformat(),
        }
        for history in histories
    ]

@router.get("/history/{user_id}")
async def get_user_history(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserHistory).where(UserHistory.user_id == user_id))
    histories = result.scalars().all()

    if not histories:
        raise HTTPException(status_code=404, detail="No history found for this user")

    return [
        {
            "id": str(history.id),
            "user_id": str(history.user_id),
            "prompt": history.prompt,
            "destination": history.destination,
            "duration": history.duration,
            "tastes": history.tastes,
            "style": history.style,
            "generated_itinerary": history.generated_itinerary,
            "created_at": history.created_at.isoformat(),
            "updated_at": history.updated_at.isoformat(),
        }
        for history in histories
    ]
