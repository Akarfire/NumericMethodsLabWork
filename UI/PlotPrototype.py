import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional, Union

def plot_from_y_dict(
    y_data_dict: Dict[str, List[float]],
    title: str = "График функций",
    x_label: str = "Номер испытания",
    y_label: str = "Значение сахаристости свёклы",
    colors: Optional[List[str]] = None,
    modes: Optional[Union[str, List[str]]] = None,
    width: int = 900,
    height: int = 600,
    show_legend: bool = True,
    grid: bool = True,
    show_markers: bool = True,
    line_width: float = 2.5,
    text_font_family: str ="Arial, sans-serif",
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
        width=width,
        height=height,
        template='plotly_white',
        showlegend=show_legend,
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='black',
            borderwidth=1
        ),
        hovermode='x unified'
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
    
    fig.write_html(way_saving_path)



# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
if __name__ == "__main__":
    print("=" * 50)
    print("ПРИМЕР 1: Простой словарь со значениями Y")
    print("=" * 50)
    
    # Создаем тестовые данные в формате: название -> список значений Y
    y_data = {
        'Синус': np.sin(np.linspace(0, 2*np.pi, 50)),
        'Косинус': np.cos(np.linspace(0, 2*np.pi, 50)),
        'Линейная': np.linspace(0, 10, 50),
        'Квадратичная': np.linspace(0, 10, 50) ** 2 / 25
    }
    
    # Простой вызов
    plot_from_y_dict(y_data, way_saving_path = "./plot1.html")
    # fig1.show()
    
    print("\n" + "=" * 50)
    print("ПРИМЕР 4: Только линии без маркеров")
    print("=" * 50)
    
    plot_from_y_dict(
        y_data_dict=y_data,
        title="Функции без маркеров",
        show_markers=False,
        line_width=3,
        way_saving_path = "./plot2.html"
    )
    
    print("\n" + "=" * 50)
    print("ПРИМЕР 5: Сохранение в файл")
    print("=" * 50)
    plot_from_y_dict(
        y_data_dict={'Тестовая функция': np.random.randn(100)},
        title="Случайные данные",
        show_legend=False,
        way_saving_path = "./plot3.html"
    )    
    
    print("\n" + "=" * 50)
    print("ПРИМЕР 7: Реальные данные")
    print("=" * 50)
    
    # Пример с реальными данными
    monthly_sales = {
        'Продажи 2023': [120, 135, 148, 165, 180, 195, 210, 205, 190, 185, 200, 220],
        'Продажи 2024': [130, 145, 160, 175, 190, 210, 225, 220, 210, 205, 215, 235],
        'Цель': [150] * 12  # Постоянная цель
    }
    
    plot_from_y_dict(
        y_data_dict=monthly_sales,
        title="Ежемесячные продажи",
        x_label="Месяц (1-12)",
        y_label="Продажи, тыс. руб.",
        colors=['blue', 'red', 'green'],
        modes=['lines+markers', 'lines+markers', 'lines'],
        width=1000,
        height=600,
        way_saving_path = "./plot4.html"
    )
