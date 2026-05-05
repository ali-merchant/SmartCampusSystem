from models.user import User

def inp():
    try:
        user = User(
            name="Ali",
            role="student",
            choice=5,
            category="AI_Lab_Support",
            current_location="Hostel",
            preferred_slot=2,
            severity=8,
            time_sensitivity=9,
            crowd_level=5,
            description_note="Need urgent help before practical evaluation",
        )
        print("Request type:", user.requestType)
    except ValueError as e:
        print("Invalid input:", e)

if __name__ == "__main__":
    inp()