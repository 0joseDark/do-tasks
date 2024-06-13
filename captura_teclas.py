import msvcrt
import time

# Abrir o arquivo txt para escrita
with open('captura_teclas.txt', 'w') as arquivo:
    while True:
        # Obter a tecla pressionada
        tecla = msvcrt.getch()

        # Converter a tecla em um caractere maiúsculo
        tecla_str = chr(tecla).upper()

        # Verificar se a tecla é uma seta, PgUp ou PgDn
        if tecla_str in ['W', 'S', 'A', 'D', 'PAGEUP', 'PAGEDOWN']:
            # Gravar a tecla e o timestamp no arquivo
            timestamp = time.time()
            arquivo.write(f'{tecla_str},{timestamp}\n')

        # Sair do loop se a tecla Esc for pressionada
        if tecla == 27:
            break

# Fechar o arquivo
arquivo.close()
