import pygame
from settings import *
pygame.init()

class button():
    def __init__(self, x, y, text):
        self.display_surface = pygame.display.get_surface()

        self.x = x 
        self.y = y
        self.text = text.split('//')
        self.font = main_font

        if len(self.text) > 1:
            self.text_surfaces = []
            self.text_rect = []
            for text in 0,1:
                text_surf = self.font.render(self.text[text], False, TEXT_COLOR)
                text_rect = text_surf.get_rect(topleft = (self.x , self.y))
                self.text_surfaces.append(text_surf)
                self.text_rect.append(text_rect)
                self.y += self.text_rect[0].height
            self.text_rect[0].height += self.text_rect[0].height
        
        else:
            self.text_surf = self.font.render(self.text[0], False, TEXT_COLOR)
            self.text_rect = self.text_surf.get_rect(center = (self.x , self.y))
            
            self.text_rect.topleft = (x,y)
        self.clicked =  False

     
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
                
        if len(self.text) > 1:
            for text in 0,1:
                if text == 0:
                    if self.text_rect[text].inflate(20,20).collidepoint(pos):
                        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.text_rect[text].inflate(20,20))
                        pygame.draw.rect(self.display_surface, UI_SELECTED_COLOR, self.text_rect[text].inflate(20,20), 3)

                        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                            self.clicked = True
                            action = True
                        if pygame.mouse.get_pressed()[0] == 0:
                            self.clicked = False
                    else:
                        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.text_rect[text].inflate(20,20))
                        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.text_rect[text].inflate(20,20), 3)

                self.display_surface.blit(self.text_surfaces[text], self.text_rect[text])

        else:
            if self.text_rect.inflate(20,20).collidepoint(pos):
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.text_rect.inflate(20,20))
                pygame.draw.rect(self.display_surface, UI_SELECTED_COLOR, self.text_rect.inflate(20,20), 3)

                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            else:
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.text_rect.inflate(20,20))
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.text_rect.inflate(20,20), 3)

            self.display_surface.blit(self.text_surf, self.text_rect)

        return action

class question():
    def __init__ (self,quest, ans1, ans2, ans3, ans4, correct):
        self.question = quest.split('//')
        self.answers = [0,0,0,0]
        self.answers[correct] = 1
        self.good = None
        self.ans1 = button(20, 80, ans1)
        self.ans2 = button(20, 160, ans2)
        self.ans3 = button(20, 240, ans3)
        self.ans4 = button(20, 320, ans4)
        self.timer = 0

        
    def draw(self):
        going = True
        draw_text(self.question[0], main_font, WHITE, 20, 10)
        if len(self.question) > 1:
            draw_text(self.question[1], main_font, WHITE, 20, 30)
        if self.ans1.draw():
            self.timer = pygame.time.get_ticks()
            if self.answers[0] == 1:
                self.good = True 
            else:
                self.good = False 
                
        if self.ans2.draw():
            self.timer = pygame.time.get_ticks()
            if self.answers[1] == 1:
                self.good = True 
            else:
                self.good = False 

        if self.ans3.draw():
            self.timer = pygame.time.get_ticks()
            if self.answers[2] == 1:
                self.good = True 
            else:
                self.good = False 

        if self.ans4.draw():
            self.timer = pygame.time.get_ticks()
            if self.answers[3] == 1:
                self.good = True 
            else:
                self.good = False 

        if self.good:
            pygame.draw.rect(screen, (0,255,0), (200,300,200,100))
            pygame.draw.rect(screen, (255,255,255), (200,300,200,100), 3)
            draw_text('Correct', font1, BLACK, 240,325)
            if pygame.time.get_ticks()-self.timer > 1000:
                self.good = None
                going = True
                return going
            
        elif self.good == False:
            pygame.draw.rect(screen, (255,0,0), (200,300,200,100))
            pygame.draw.rect(screen, (255,255,255), (200,300,200,100), 3)
            draw_text('Incorrect.', font1, BLACK, 240,310)
            draw_text('Try Again', font1, BLACK, 240, 340)
            if pygame.time.get_ticks()-self.timer > 1000:
                self.good = None

question_list = [
        question('¿Qué es la inteligencia artificial (IA)?',
         'a) Es la capacidad de las máquinas para pensar y sentir como los humanos.',
         'b) Son exclusivamente aquellos robots que pueden realizar tareas humanas de forma //autónoma',
         'c) Es solo un concepto de ciencia ficción sin aplicaciones reales en el mundo actual.',
         'd) Un campo de la informática que se enfoca en crear sistemas con la capacidad de//aprender de conjuntos de datos, reconocer patrones y tomar decisiones.',
         3),
    question('¿Cuál es una preocupación ética común relacionada con el desarrollo de la// inteligencia artificial??',
         'a) El aumento de la productividad y la eficiencia.',
         'b) La creación de trabajos especializados en IA.',
         'c) Los sesgos y la discriminación en los resultados',
         'd) La expansión del acceso a la atención médica.',
         2),
    question('¿Qué es un sesgo algorítmico?',
         'a) la tendencia de los algoritmos a producir resultados imparciales y equitativos',
         'b) Se refiere algoritmos que tienden a producir resultados aleatorios en lugar de seguir un// patrón predecible.',
         'c) Es un término que describe la capacidad de un algoritmo para adaptarse y aprender de// forma autónoma.',
         'd) la tendencia de un sistema a reflejar los jucios humanos, lo que puede llevar a// decisiones sesgadas o resultados perjudiciales.',
         3),
    question('¿Cómo se puede evitar que un sistema de IA manipule el flujo de la información para influir// en elecciones políticas?',
         'a) Implementar medidas de censura que atenten contra la libertad de expresión. ',
         'b) Permitir que las empresas utilicen IA libremente para influir en la democracia.',
         'c) Fomentar el uso consciente y crítico de la información y desarrollar contramedidas //tecnológicas para disminuir la desinformación.',
         'd) No intervenir y dejar que la manipulación continúe por el bien de //la libertad de expresión.',
         2),
    question('¿Qué enfoque es el más corrrecto cuando un algoritmo de salud predice mal la //condición de un paciente?',
         'a) Divulgar la limitación del algoritmo y ofrecer una solución alternativa.',
         'b) Ocultar el error para evitar dañar la reputación del algoritmo.',
         'c) Mejorar el algoritmo sin informar sobre el error inicial.',
         'd) Culpar al usuario por confiar en el algoritmo sin verificar con un médico.',
         0),
    question('¿Qué opción es la menos ética cuando un algoritmo de contratación discrimina a //candidatos basándose en su género?',
         'a) Modificar el algoritmo para corregir la discriminación.',
         'b) Ignorar el problema y continuar utilizando el algoritmo actual.',
         'c) Desarrollar un algoritmo alternativo que no discrimine.',
         'd) Ajustar los datos de entrada para equilibrar las predicciones del algoritmo.',
         1),
    question('Una red social ha creado un algoritmo que promueve contenido extremo y polarizado.// ¿Qué acción sería más ética?',
         'a) Mantener el algoritmo sin cambios.',
         'b) Hacer ajustes menores para reducir la polarización.',
         'c) Detener el uso del algoritmo.',
         'd) Revelar abiertamente los efectos y reformular el algoritmo para un ambiente más //saludable.',
         3),
    question('¿Cuál es el papel de los comités de ética en el desarrollo de tecnologías de //inteligencia artificial?',
         'a) Desempeñan un papel crucial al asegurar que los proyectos de IA se adhieran a //estándares éticos y morales aceptados.',
         'b) No son necesarios en el desarrollo de IA, ya que la ética es subjetiva',
         'c) Obstaculizar la innovación en IA al imponer restricciones innecesarias.',
         'd) Son responsables de garantizar la rentabilidad de los proyectos de IA y deben //priorizar los intereses comerciales sobre los éticos.',
         0),
    question('¿Cuál es uno de los principales desafíos al reemplazar las interacciones //sociales humanas con inteligencia artificial?',
         'a) La promoción de la inclusión y la diversidad.',
         'b) La pérdida de conexiones significativas y genuinas.',
         'c) La mejora de la calidad de vida de las personas.',
         'd) La aceleración del progreso tecnológico.',
         1),
    question('Qué impacto tendrá el desarrollo de la inteligencia artificial en //las próximas décadas?',
         'a) El surgimiento de preocupaciones éticas y sociales sobre el control y //el uso responsable de la IA.',
         'b) La transformación radical de distintos ámbitos del mundo, como la salud,// la educación y la política.',
         'c) La posibilidad de alcanzar avances científicos y tecnológicos sin precedentes.',
         'd) Todas las anteriores',
         3),
]