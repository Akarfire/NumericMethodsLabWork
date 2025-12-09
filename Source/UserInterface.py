from Results import Results
from Input import Input, DegradationMode
from Data import Statistics

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
from typing import Dict, List, Optional, Union

import sys, json
from dataclasses import fields


class UserInterface:
    
    def __init__(self, core):
        self.core = core
        self.userDataPath : str = "./"
        
    # Listening to the input from the frontend
    def run_ui(self):
        
        for line in sys.stdin:
            
            try:
                msg = json.loads(line)
                
                if "user_data_path" in msg:
                    self.userDataPath = msg["user_data_path"]
                    print(self.userDataPath)
                    continue
                
                if "input_data" in msg:
                    input_data_dict = msg["input_data"]
                    print(input_data_dict)
                    self.core.call_run(self.__convert_dict_to_input_data(input_data_dict))
                
                else:
                    self.__send_message({"Error" : "No input data provided"})
                    
            except Exception as e:
                self.__send_message({"Error" : str(e)})
    
    
    # Sends results of the calculations back to the frontend
    def send_results(self, results : Results):
        
        # Generating plot
        self.__generate_plot(results)
        
        # Sending results message
        self.__send_message({"results" : self.__convert_results_data_to_dict(results)})
    
    
    # Sends a message through standard output
    @staticmethod
    def __send_message(message):
        sys.stdout.flush()
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
    
    
    # Converts dictionary, received from the frontend into an input data structure
    @staticmethod
    def __convert_dict_to_input_data(input_data_dict : dict) -> Input:
           
        kwargs = {}
        for f in fields(Input):
            name = f.name

            if name not in input_data_dict:
                continue  # use default

            val = input_data_dict[name]
            
            kwargs[name] = val
            
        degradation_mode_map = {
            "UNIFORM" : DegradationMode.UNIFORM,
            "CONCENTRATED" : DegradationMode.CONCENTRATED
        }
        if "degradation_mode" in input_data_dict:
            mode_name =  input_data_dict["degradation_mode"]
            if mode_name in degradation_mode_map:
                kwargs["degradation_mode"] = degradation_mode_map[mode_name]
        
        return Input(**kwargs)
    
    
    # Converts results data structure into a dictionary for sending
    @staticmethod
    def __convert_results_data_to_dict(results_data : Results) -> dict:
        
        results_dict = dict()
        results_dict["best_strategy"] = results_data.best_strategy
        results_dict["worst_strategy"] = results_data.worst_strategy
        results_dict["statistics_list"] = results_data.statistics_list
        
        return results_dict
    
    
    def __generate_plot(self, results : Results):
        
        my_template = dict(
            layout=dict(
                font=dict(family="Arial, Helvetica, sans-serif", color="white"),
                paper_bgcolor="rgba(0.0, 0.0, 0.0, 0.0)",
                plot_bgcolor="rgba(0.0, 0.0, 0.0, 0.0)",
                xaxis=dict(gridcolor="#333", zerolinecolor="#555"),
                yaxis=dict(gridcolor="#333", zerolinecolor="#555"),
                legend=dict(    bgcolor="rgba(0.0, 0.0, 0.0, 0.0)",
                                borderwidth=0,
                                bordercolor="rgba(0.0, 0.0, 0.0, 0.0)")
            )
        )

        pio.templates["custom"] = my_template
        
        # Plot logic by LeoGNZV
        def plot_from_y_dict(
            y_data_dict: Dict[str, List[float]],
            title: str = "График сахаристости по этапам переработки",
            x_label: str = "",
            y_label: str = "Сахаристость свёклы",
            colors: Optional[List[str]] = None,
            modes: Optional[Union[str, List[str]]] = None,
            width: int = 900,
            height: int = 600,
            show_legend: bool = True,
            grid: bool = True,
            show_markers: bool = True,
            line_width: float = 2.5,
            text_font_family: str ="Arial, Helvetica, sans-serif",
            way_saving_path: str = "./plot.html"
        ) -> go.Figure:
            """
            Создает график из словаря, где ключи - названия функций, 
            а значения - списки/массивы значений Y.
            
            Параметры:
            ----------
            y_data_dict : dict
                Словарь формата {'название_функции1': [y1, y2, ...], ...}
                Где X автоматически становится [0, 1, 2, ..., len(y)-1]
            title : str, optional
                Заголовок графика.
            x_label : str, optional
                Подпись оси X.
            y_label : str, optional
                Подпись оси Y.
            colors : list of str, optional
                Цвета для каждого графика.
            modes : str or list of str, optional
                Тип отображения: 'lines', 'markers', 'lines+markers'.
            width : int, optional
                Ширина графика в пикселях.
            height : int, optional
                Высота графика в пикселях.
            show_legend : bool, optional
                Показывать ли легенду.
            grid : bool, optional
                Показывать ли сетку.
            show_markers : bool, optional
                Показывать ли маркеры на графиках.
            line_width : float, optional
                Толщина линий на графиках.
            
            Возвращает:
            -----------
            fig : plotly.graph_objects.Figure
                Объект Figure для отображения или дальнейшей настройки.
            """
            
            # Проверяем, что словарь не пустой
            if not y_data_dict:
                raise ValueError("Словарь данных не должен быть пустым")
            
            # Подготавливаем списки для данных
            x_data_list = []
            y_data_list = []
            labels = []
            
            # Обрабатываем каждый элемент словаря
            for label, y_values in y_data_dict.items():
                # Преобразуем в numpy array для единообразия
                y_array = np.array(y_values)
                
                # Создаем массив X как индексы элементов Y
                x_array = np.arange(len(y_array))
                
                # Сохраняем данные
                labels.append(label)
                x_data_list.append(x_array)
                y_data_list.append(y_array)
            
            # Проверяем, что все массивы Y имеют одинаковую длину (опционально, можно закомментировать)
            lengths = [len(y) for y in y_data_list]
            if len(set(lengths)) > 1:
                print(f"Внимание: массивы Y имеют разную длину: {lengths}")
                print("Графики будут построены с разным количеством точек")
            
            # Устанавливаем значения по умолчанию для цветов
            if colors is None:
                color_sequence = px.colors.qualitative.Plotly
                colors = [color_sequence[i % len(color_sequence)] for i in range(len(labels))]
            
            # Устанавливаем режим отображения
            if modes is None:
                if show_markers:
                    modes = ['lines+markers'] * len(labels)
                else:
                    modes = ['lines'] * len(labels)
            elif isinstance(modes, str):
                # Если передан один строковый параметр, применяем ко всем графикам
                modes = [modes] * len(labels)
            
            # Создаем график
            fig = go.Figure()
            
            # Добавляем каждый набор данных на график
            for i in range(len(labels)):
                fig.add_trace(go.Scatter(
                    x=x_data_list[i],
                    y=y_data_list[i],
                    mode=modes[i],
                    name=labels[i],
                    line=dict(color=colors[i], width=line_width),
                    marker=dict(size=8 if 'markers' in modes[i] else 0),
                    opacity=0.9
                ))
            
            # Настраиваем макет
            fig.update_layout(
                title=dict(
                    text=title,
                    x=0.5,
                    font=dict(size=22, family=text_font_family)
                ),
                xaxis_title=dict(
                    text=x_label,
                    font=dict(size=14)
                ),
                yaxis_title=dict(
                    text=y_label,
                    font=dict(size=14)
                ),
                # width=width,
                # height=height,
                autosize=True,
                template='custom',
                showlegend=show_legend,
                legend=dict(
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                ),
                hovermode='closest',
                hoverlabel=dict(
                    bgcolor="rgba(0, 0, 0, 0.8)",
                )
            )
            
            # Настройка осей
            if grid:
                fig.update_xaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='LightGray',               
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='LightGray'
                )
                fig.update_yaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='LightGray',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='LightGray'
                )
            else:
                fig.update_xaxes(showgrid=False, zeroline=False)
                fig.update_yaxes(showgrid=False, zeroline=False)
            
            html = fig.to_html(include_plotlyjs="cdn", full_html=True, config={"responsive": True})

            injected = """
            <style>
            html, body {overflow:hidden !important; margin:0; padding:0;}
            .plot-container, .js-plotly-plot, .plotly {
                width:100% !important; height:100% !important; overflow:hidden !important;
            }
            
            .hoverlayer g.hovertext rect {
                fill: rgba(0,0,0,0.85) !important;
                stroke: rgba(255,255,255,0.06) !important;
            }
            
            .hoverlayer .hoverlabel, .hoverlayer .hoverlabel * {
                background-color: rgba(0,0,0,0.85) !important;
                color: white !important;
            }
            
            </style>
            <script>
            let rt;
            window.addEventListener("resize", () => {
                clearTimeout(rt);
                rt = setTimeout(() => {
                    Plotly.Plots.resize(document.querySelector('.js-plotly-plot'));
                }, 50);
            });
            </script>
            """
            html = html.replace("</head>", injected + "</head>")
            
            with open(way_saving_path, "w", encoding="utf-8") as f:
                f.write(html)

        # Calling plot generation
        plot_from_y_dict(results.statistics, way_saving_path = self.userDataPath + "/plot.html")