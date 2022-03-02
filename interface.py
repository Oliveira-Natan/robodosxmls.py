import PySimpleGUI as sg
from consultadeversao import consultadeversao
from robodaspastas_v01_2022 import robodaspastas
from robodoonedriver_v01_2022 import robodoonedriver
from robodospdfs_v01_2022 import robodospdfs
from robodeindividualizacao_v01_2022 import robodeindividualizacao
from robodosemailsparaarquivei_v01_2022 import robodosemailsparaarquivei

'pyi-makespec interface.py --onefile --icon=logo.ico --name mcstoolsdesktop_retidos'
'pyinstaller --clean mcstoolsdesktop_retidos.spec'
# ao mover o programa para outra pasta, o icone deixa de ser python e vira icon

sg.theme('DarkTeal12')  # Add a touch of color

consulta_de_versao = consultadeversao()
# consulta_de_versao = 'versao_atualizada'
if consulta_de_versao == 'versao_atualizada':
    layout = [[sg.Text('MCS Tools Desktop: Retidos', justification='center', size=(25, 1))],
              [sg.Button('Robo das Pastas', size=(25, 1))],
              [sg.Button('Robo do OneDriver', size=(25, 1))],
              [sg.Button('Robo dos PDFs', size=(25, 1))],
              [sg.Button('Robo de Individualização', size=(25, 1))],
              [sg.Button('Robo de emails pra Arquivei', size=(25, 1))],
              ]
    win1 = sg.Window('MCS Tools Desktop: Retidos', layout)

    while True:
        event, value = win1.read(timeout=100)
        if event == 'Robo das Pastas':
            robodaspastas()
        elif event == 'Robo do OneDriver':
            robodoonedriver()
        elif event == 'Robo dos PDFs':
            robodospdfs()
        elif event == 'Robo de Individualização':
            robodeindividualizacao()
        elif event == 'Robo de emails pra Arquivei':
            robodosemailsparaarquivei()

        if event == sg.WIN_CLOSED:
            break

else:
    layout = [[sg.Text('MCS Tools Desktop: Retidos', justification='center', size=(35, 1))],
              [sg.Text('Ops, a sua versão está desatualizada.\n'
                       'Entre em contato com a Inovação da MCS \n'
                       'para baixar a nova versão.',
                       justification='center', size=(35, 3))]
              ]
    win1 = sg.Window('MCS Tools Desktop: Retidos', layout)

    while True:
        event, value = win1.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
