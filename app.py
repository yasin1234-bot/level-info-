from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

LEVELS = {
"1":0,"2":48,"3":202,"4":544,"5":1012,"6":1844,"7":2792,"8":3800,"9":4870,"10":6004,
"11":7192,"12":8448,"13":9776,"14":11140,"15":12566,"16":14060,"17":15610,"18":17224,
"19":18902,"20":20632,"21":22424,"22":24728,"23":26192,"24":28166,"25":30200,"26":32294,
"27":34448,"28":37804,"29":41174,"30":44870,"31":48852,"32":53334,"33":58566,"34":64096,
"35":69994,"36":76460,"37":83108,"38":91128,"39":99322,"40":108092,"41":120144,"42":133266,
"43":147472,"44":162760,"45":179126,"46":196572,"47":215368,"48":235516,"49":257010,
"50":279860,"51":304056,"52":348318,"53":394982,"54":444044,"55":495508,"56":549364,
"57":633756,"58":721744,"59":813336,"60":908522,"61":1041438,"62":1180352,"63":1325256,
"64":1476184,"65":1634300,"66":1840946,"67":2056594,"68":2281242,"69":2514880,"70":2757530,
"71":3059506,"72":3372284,"73":3699456,"74":4041030,"75":4397020,"76":4829104,"77":5282204,
"78":5756304,"79":6251404,"80":6767504,"81":7381324,"82":8043154,"83":8752952,"84":9510808,
"85":10316638,"86":11277190,"87":12360748,"88":13360304,"89":14482858,"90":15659418,
"91":17026708,"92":18453688,"93":19941280,"94":21488570,"95":23095858,"96":24763138,
"97":26490138,"98":28277708,"99":30124996,"100":32032284
}

def get_exp_for_level(level):
    return LEVELS.get(str(level), 0)


def fetch_player(uid):
    try:
        url = f"https://flash-info-cbw4.vercel.app/info?uid={uid}&key=Flash"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()
        return data

    except:
        return None


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire Level API Working",
        "endpoint": "/level/<uid>?key=Flash"
    })


@app.route("/level/<uid>")
def level(uid):

    key = request.args.get("key")

    if key not in ["Flash", "DENGER"]:
        return jsonify({
            "success": False,
            "message": "Invalid Key"
        })

    player = fetch_player(uid)

    if not player:
        return jsonify({
            "success": False,
            "message": "Player API Down"
        })

    try:
        info = player.get("basicInfo", {})

        nickname = info.get("nickname", "Unknown")
        level = int(info.get("level", 0))
        exp = int(info.get("exp", 0))

        next_exp = get_exp_for_level(level + 1)
        current_exp = get_exp_for_level(level)

        if next_exp == 0:
            return jsonify({
                "success": True,
                "uid": uid,
                "nickname": nickname,
                "level": level,
                "message": "Max Level"
            })

        need = next_exp - exp
        percent = ((exp - current_exp) / (next_exp - current_exp)) * 100

        return jsonify({
            "success": True,
            "uid": uid,
            "nickname": nickname,
            "level": level,
            "current_exp": exp,
            "exp_for_next_level": next_exp,
            "exp_needed": need,
            "progress": round(percent,1)
        })

    except:
        return jsonify({
            "success": False,
            "message": "Data Parse Error"
        })


@app.route("/levels")
def levels():
    return jsonify({
        "success": True,
        "levels": LEVELS
    })


if __name__ == "__main__":
    app.run()