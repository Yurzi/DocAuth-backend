from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO
import os.path
# 将public下的字体文件拷贝到第三方包的目录下，如：
# site-packages\reportlab\fonts下
pdfmetrics.registerFont(TTFont('SimSun', os.path.join('public','SimSun.ttf')))  # 默认不支持中文，需要注册字体

stylesheet = getSampleStyleSheet()   # 获取样式集

# 获取reportlab自带样式
Normal = stylesheet['Normal']
BodyText = stylesheet['BodyText']
Italic = stylesheet['Italic']
Title = stylesheet['Title']
Heading1 = stylesheet['Heading1']
Heading2 = stylesheet['Heading2']
Heading3 = stylesheet['Heading3']
Heading4 = stylesheet['Heading4']
Heading5 = stylesheet['Heading5']
Heading6 = stylesheet['Heading6']
Bullet = stylesheet['Bullet']
Definition = stylesheet['Definition']
Code = stylesheet['Code']
 
# 自带样式不支持中文，需要设置中文字体，但有些样式会丢失，如斜体Italic。有待后续发现完全兼容的中文字体
Normal.fontName = 'SimSun'
Italic.fontName = 'SimSun'
BodyText.fontName = 'SimSun'
Heading1.fontName = 'SimSun'
Heading2.fontName = 'SimSun'
Heading3.fontName = 'SimSun'
Heading4.fontName = 'SimSun'
Heading5.fontName = 'SimSun'
Heading6.fontName = 'SimSun'
Bullet.fontName = 'SimSun'
Definition.fontName = 'SimSun'
Code.fontName = 'SimSun'
 
# 添加自定义样式
stylesheet.add(
    ParagraphStyle(name='body',
                   fontName="SimSun",
                   fontSize=10,
                   textColor='black',
                   leading=20,                # 行间距
                   spaceBefore=0,             # 段前间距
                   spaceAfter=10,             # 段后间距
                   leftIndent=0,              # 左缩进
                   rightIndent=0,             # 右缩进
                   firstLineIndent=20,        # 首行缩进，每个汉字为10
                   alignment=TA_JUSTIFY,      # 对齐方式
 
                   # bulletFontSize=15,       #bullet为项目符号相关的设置
                   # bulletIndent=-50,
                   # bulletAnchor='start',
                   # bulletFontName='Symbol'
                   )
            )
Body = stylesheet['body']

styleMap = {
  'normal':Normal,
  'bodyText':BodyText,
  'italic':Italic,
  'title':Title,
  'h1':Heading1,
  'h2':Heading2,
  'h3':Heading3,
  'h4':Heading4,
  'h5':Heading5,
  'h6':Heading6,
  'bullet':Bullet,
  'definition':Definition,
  'code':Code,
  'body':Body
}

def createPdfBuf(contents:list[list[str]]):
  story = []
  for content in contents:
    style = styleMap[content[1]]
    story.append(Paragraph(content[0], style))

  # bytes
  buf = BytesIO()
  doc = SimpleDocTemplate(buf, encoding='UTF-8')
  doc.build(story)
  # print(buf.getvalue().decode())
  
  # file
  # doc = SimpleDocTemplate('hello.pdf')
  # doc.build(story)
  return buf
 

 

 
