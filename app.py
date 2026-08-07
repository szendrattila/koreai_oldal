from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Grammar data structure transferred to Python backend
GRAMMAR_UNITS = {
    "Unit 1 · Greetings": {
        "G1: N은/는 N이에요/예요 (Topic & Copula)": [
            {"en": "I am a doctor.", "slots": [[{"t": "저", "ok": True, "isParticle": False}], [{"t": "는", "ok": True, "isParticle": True}, {"t": "은", "ok": False, "isParticle": True}], [{"t": "의사", "ok": True, "isParticle": False}], [{"t": "예요", "ok": True, "isParticle": True}, {"t": "이에요", "ok": False, "isParticle": True}]]},
            {"en": "Is Yujin a student?", "slots": [[{"t": "유진 씨", "ok": True, "isParticle": False}], [{"t": "는", "ok": True, "isParticle": True}, {"t": "은", "ok": False, "isParticle": True}], [{"t": "학생", "ok": True, "isParticle": False}], [{"t": "이에요?", "ok": True, "isParticle": True}, {"t": "예요?", "ok": False, "isParticle": True}]]},
            {"en": "The teacher is Korean.", "slots": [[{"t": "선생님", "ok": True, "isParticle": False}], [{"t": "은", "ok": True, "isParticle": True}, {"t": "는", "ok": False, "isParticle": True}], [{"t": "한국 사람", "ok": True, "isParticle": False}], [{"t": "이에요", "ok": True, "isParticle": True}, {"t": "예요", "ok": False, "isParticle": True}]]}
        ],
        "G2: N이/가 아니에요 (Negative Copula)": [
            {"en": "I am not a singer.", "slots": [[{"t": "저", "ok": True, "isParticle": False}], [{"t": "는", "ok": True, "isParticle": True}, {"t": "은", "ok": False, "isParticle": True}], [{"t": "가수", "ok": True, "isParticle": False}], [{"t": "가", "ok": True, "isParticle": True}, {"t": "이", "ok": False, "isParticle": True}], [{"t": "아니에요", "ok": True, "isParticle": False}]]}
        ]
    },
    "Unit 2 · Classroom & Room": {
        "G1: 이거/그거/저거는 N이에요/예요 (Demonstratives)": [
            {"en": "This is a pencil case.", "slots": [[{"t": "이거", "ok": True, "isParticle": False}], [{"t": "는", "ok": True, "isParticle": True}, {"t": "은", "ok": False, "isParticle": True}], [{"t": "필통", "ok": True, "isParticle": False}], [{"t": "이에요", "ok": True, "isParticle": True}, {"t": "예요", "ok": False, "isParticle": True}]]}
        ]
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/grammar/topics", methods=["GET"])
def get_topics():
    unit = request.args.get("unit")
    if unit in GRAMMAR_UNITS:
        topics = list(GRAMMAR_UNITS[unit].keys())
        return jsonify({"topics": topics})
    return jsonify({"topics": []})

@app.route("/api/grammar/exercise", methods=["GET"])
def get_exercise():
    unit = request.args.get("unit")
    topic = request.args.get("topic", "ALL")

    unit_topics = GRAMMAR_UNITS.get(unit, {})
    if not unit_topics:
        return jsonify({"error": "Unit not found"}), 404

    if topic == "ALL" or topic not in unit_topics:
        pool = [ex for exercises in unit_topics.values() for ex in exercises]
    else:
        pool = unit_topics.get(topic, [])

    if not pool:
        return jsonify({"error": "No exercises found"}), 404

    exercise = random.choice(pool)
    return jsonify(exercise)

if __name__ == "__main__":
    app.run(debug=True, port=5000)