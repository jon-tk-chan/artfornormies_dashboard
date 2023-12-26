import streamlit as st
import plotly.graph_objects as go
from io import BytesIO

# Colors were selected using imagecolorpicker.com
#colors from selected photos from Greg Girard's photography work: https://bluelotus-gallery.com/#/greg-girard/
ggBeige = '#c8a398'
ggBlack = '#18171a'
ggBrownLight = '#78554e'
ggGreenLight = '#73a8a8'
ggGreenDark = '#466863'
ggRedDark = '#b2263f'
ggRedLight = '#f39591'
ggBrownDark = '#4e3832'
ggBlueLight = '#597f9e'
ggBlueDark = '#485061'
#colors inspired by Chinatown in Vancouver, BC
yvr_medYellow = '#fcbe11'
yvr_medGreen = '#197059'
yvr_darkRed = '#b80807'
yvr_darkWhite = '#e9e3dc'
yvr_darkYellow = '#f4a002'
#ORIGINAL: color codes for HK Taxis
hk_red = "#A8102A"
hk_green = '#7bedda'
hk_blue = '#1076a8'

# hk_pm = [ggBeige, ggBlack, ggBrownLight, ggGreenLight, ggGreenDark, ggRedDark, ggRedLight, ggBrownDark, ggBlueLight, ggBlueDark]
color_combos = {
    "Espresso (brown/black)": [ggBrownLight, ggBlack],
    "Pinky (pink/green)": [ggRedLight, ggGreenDark],
    "Blush (pink/red)":[ggRedLight, ggRedDark],
    "Pacific (blue/green)" : [ggBlueDark, ggGreenLight],
    # "HK Taxi MUTED (blue/red)" :[ggBlueLight,ggRedDark],
    "Nougat (beige/brown)": [ggBeige, ggBrownDark],
    "HK Taxi (blue/red)":[hk_blue, hk_red],
    "Chinatown Bakery (yellow/turquoise)": [yvr_medYellow, yvr_medGreen],
    "Dim Sum (yellow/red)": [yvr_darkYellow, yvr_darkRed]
 }

data_font='Futura'
title_font='Futura'
anno_text_default = "Source: <i>https://github.com/jon-tk-chan</i><br><i>Instagram: @artfornormies</i>"

#NEWLINED FUNCTION - for inserting breaks into text labels for graphs
def newlined(input_string, max_line_len=12):
    """Return a string with line breaks added when line length reaches max_line_len.
    
    This function is useful for formatting individual plotly labels, especially when
    dealing with scatter plots.
    
    Args:
        input_string (str): The input string to be formatted.
        max_line_len (int, optional): The maximum desired line length before adding a line break.
            Defaults to 12.
    
    Returns:
        str: The formatted string with line breaks added.
    """
    
    curr_line_len = 0
    out_str = ""
    for i, char in enumerate(input_string):
        curr_line_len += 1
        if char == " " and curr_line_len >= max_line_len:
            out_str += "<br>"
            curr_line_len = 0
        else: 
            out_str += char
        
    return out_str


def create_venn_2(venn_labels=["LEFT", "RIGHT","MID"], fill_venn=False, 
                  left_color=hk_blue, right_color=hk_red, opacity_val = 0.5,
                  label_charlen=10,

                  main_title="VENN_TITLE",anno_text=anno_text_default,night_mode=False,
                  fig_width=1000, fig_height=1200, label_size=28):
    """Generate a Plotly Figure of a 2-circle Venn diagram with labeled regions.
    
    Args:
        venn_labels (list): Labels for the Venn diagram regions [left, right, middle intersection].
            Default is ["LEFT", "RIGHT", "MID"].
        fill_venn (bool): Whether to fill Venn diagram regions with colors. Default is False.
        left_color (str): Predefined color for the left Venn region. Default is hk_blue.
        right_color (str): Predefined color for the right Venn region. Default is hk_red.
        label_charlen (int): Maximum character length for each label. Default is 10.
        main_title (str): Title for the Venn diagram figure. Default is "VENN_TITLE".
        anno_text (str): Annotation text displayed below the Venn diagram. Default is anno_text_default.
        night_mode (bool): Use night mode color scheme. Default is False.
        fig_width (int): Width of the figure in pixels. Default is 1000.
        fig_height (int): Height of the figure in pixels. Default is 1200.
        label_size (int): Font size for the labels. Default is 28.
    
    Returns:
        go.Figure: A Plotly Figure containing the 2-circle Venn diagram.
    """
    title_size = 32 #not referenced?
    # label_size = 30
    anno_size = 14
    if not night_mode:
        outline_color="black"
        font_color="black"
        bg_color="white"
        # opacity_val = 0.25
        line_color="black"
       
    else:
        outline_color="white"
        font_color="white"
        bg_color="black"
        # opacity_val = 0.7
        line_color="white"
        
    if not fill_venn:
        left_fill = None
        right_fill = None
        line_weight=7
    else:
        left_fill = left_color
        right_fill = right_color
        line_weight=3
    data_dict = {
        "x": [1,2,3],
        "y": [1,1,1],
            "text": [newlined(venn_labels[0], label_charlen), newlined(venn_labels[2],label_charlen),newlined(venn_labels[1],label_charlen)]
    }
    fig = go.Figure()

    ### ADD VENN DIAGRAMS
    fig.add_trace(go.Scatter(
        x = data_dict["x"],
        y = data_dict["y"],
        text = data_dict['text'],
        mode="text",
        textfont=dict(
            color=font_color,
            size=label_size,
            family=data_font,
        )
    ))
    fig.add_shape(type="circle",
        line_color=line_color, line_width=line_weight,
                  fillcolor=left_fill,
        x0=0.5, y0=0, x1=2.5, y1=2,
                  layer='below'
    )
    fig.add_shape(type="circle",
        line_color=line_color, line_width=line_weight,
                  fillcolor=right_fill,
        x0=1.5, y0=0, x1=3.5, y1=2,
                  layer='below'
    )

    fig.update_shapes(opacity=opacity_val, xref="x", yref="y")

    # Update axes properties
    fig.update_xaxes(showticklabels=False,showgrid=False,zeroline=False,
    )

    fig.update_yaxes(showticklabels=False,showgrid=False,zeroline=False,
    )

    fig.update_layout(
        title=main_title,
        font=dict(family=data_font, size=title_size,color=font_color),
        plot_bgcolor=bg_color, paper_bgcolor=bg_color,
        height=fig_height, #use width for height so that image is not stretched
        width=fig_width,
        margin=dict(l=20, r=20, b=100),
    )

    #add annotation
    fig.add_annotation(
        text = anno_text, showarrow=False,
        x = 0.04, y = -0.1125, #controls how far from axes 
        xref='paper', yref='paper' , xanchor='left', yanchor='bottom',
        font=dict(size=anno_size), align="left",
    )

    return fig

###### START DASHBOARD CODE - DEFAULT HEADER #######
st.markdown("## Two Things Can Be True - Venn Diagram Maker")
st.markdown("##### Instagram: @artfornormies")
st.markdown("""     
    *Scroll down and press the 'Download image' button to save your venn diagram image in PNG format.* 
            
    Dashboard for creating venn diagrams and exporting images for social media/personal use. Intended uses include making mental health reminders for content creation (social media posts, blog post headers, etc) OR for personal use (phone wallpapers).

""")

#### SIDEBAR VERSION

with st.sidebar:
    st.markdown("*please hit 'enter' to apply input changes*")
    st.markdown("# MAIN INPUTS")
    
    left_text = st.text_input("left text:", value='LEFT')
    right_text= st.text_input("right side text:", "RIGHT")
    center_text = st.text_input("center text:", value='CENTER')
    color_key = st.selectbox("Select fill colors:", color_combos.keys(), index=5)
    st.text("") #spacer
    st.markdown("# OPTIONAL INPUTS")
    title_text = st.text_input("title text:", value="")
    opacity_val = st.slider(label='select an opacity value:', 
                            min_value=0.0, max_value=1.0, value = 0.7)
    max_text_width = st.slider(label='select max length of text line (char):', 
                            min_value=0, max_value=50, value = 10)
    image_dims = st.select_slider('select edge length and width (px): ', 
                                options=[500, 600, 700, 800, 900, 1000, 1100, 1200],
                                value=700)
    lab_size = st.slider('select label font size:',
                        min_value=8, max_value=50,value=28)
        
color_left = color_combos[color_key][0]
color_right = color_combos[color_key][1]

fig = create_venn_2( venn_labels=[left_text, right_text, center_text], 
                        night_mode=True, fill_venn=True,
                        left_color=color_left, right_color=color_right, opacity_val=opacity_val,
                        label_charlen=max_text_width,
                        main_title=title_text, fig_width=image_dims, fig_height=image_dims,
                        label_size=lab_size)
#display graph
st.plotly_chart(fig)
#save image button
fig_img = fig.to_image(format='png')
btn = st.download_button(
        label="Download image",
        data=fig_img,
        file_name="artfornormies_venn.png",
        mime="image/png"
        )
st.markdown("""
    ##### References
            
Inspired by the [Collab Fund article](https://collabfund.com/blog/true-at-once/) - "Two Things Can Be True At Once" by Morgan Housel. Fill color palettes are inspired by the photography work of [Greg Girard](https://bluelotus-gallery.com/#/greg-girard/).
- Data visualizations: [Plotly - Python](https://plotly.com/python/) 
- Dashboard inteface: [Streamlit](https://docs.streamlit.io/) / [Streamlit Community Cloud](https://streamlit.io/cloud)

*Designed by Jonathan Chan: [Github](https://github.com/jon-tk-chan) / [Website](https://www.jonathantkchan.com/)*
            
""")