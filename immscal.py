from flask import Flask, render_template, request

app = Flask(__name__)

SALARIO_MIN = 9917.10
SALARIO_MAX = 87982.50

FACTOR_TRABAJADOR = 0.02375
FACTOR_PATRON = 0.202488
FACTOR_INFONAVIT = 0.05


PERIODOS = {

"Mensual":{

"trabajador":1,
"patron":1,
"infonavit":1

},

"Bimestral":{

"trabajador":2.0165,
"patron":2.0224,
"infonavit":2.01648

},

"Semestral":{

"trabajador":6.0494,
"patron":6.0675,
"infonavit":6.04946

},

"Anual":{

"trabajador":12.0658,
"patron":12.1016,
"infonavit":12.06582

}

}


def validar_salario(salario):

    if salario < SALARIO_MIN:

        raise ValueError(
            f"Salario mínimo ${SALARIO_MIN:,.2f}"
        )

    if salario > SALARIO_MAX:

        raise ValueError(
            f"Salario máximo ${SALARIO_MAX:,.2f}"
        )


def calcular_periodo(
salario,
periodo
):

    datos=PERIODOS[periodo]

    trabajador=(
    salario
    *FACTOR_TRABAJADOR
    *datos["trabajador"]
    )

    patron=(

    salario
    *FACTOR_PATRON
    *datos["patron"]

    )

    infonavit=(

    salario
    *FACTOR_INFONAVIT
    *datos["infonavit"]

    )

    total=(

    trabajador
    +patron
    +infonavit

    )

    return{

    "trabajador":
    round(trabajador,2),

    "patron":
    round(patron,2),

    "infonavit":
    round(infonavit,2),

    "total":
    round(total,2)

    }


@app.route(
"/",
methods=["GET","POST"]
)
def inicio():

    resultados=None
    error=None

    if request.method=="POST":

        try:

            salario=float(
            request.form[
            "salario"
            ]
            )

            validar_salario(
            salario
            )

            resultados={}

            for periodo in PERIODOS:

                resultados[
                periodo
                ]=(

                calcular_periodo(
                salario,
                periodo
                )

                )

        except Exception as e:

            error=str(e)

    return render_template(

    "index.html",

    resultados=resultados,

    error=error

    )


if __name__=="__main__":

    app.run(
    debug=True
    )