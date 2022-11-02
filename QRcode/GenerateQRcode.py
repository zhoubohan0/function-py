import argparse
# 二维码生成
'''
About error-correction:
four levels of error correction, referred to as L, M, Q and H respectively in increasing order of recovery capacity
    elLowest: Indicates to use the ECC level L, up to 7% (approx.) damage can be corrected.
    elMedium: Indicates to use the ECC level M, up to 15% (approx.) damage can be corrected.
    elQuality: Indicates to use the ECC level Q, up to 25% (approx.) damage can be corrected.
    elHighest: Indicates to use the ECC level H, up to 30% (approx.) damage can be corrected.
'''
def createQRcode(content,outputfile,bg=None,colorful=True):
    from MyQR import myqr
    myqr.run(words=content,                                     # 目前仅支持链接或英文文本
             version=10,                                        # 二维码的格子大小[1,40]，数值越大格子越大，一般10，
             level='Q',                                         # 25%容错
             picture=bg,                                        # 背景图片，None则为光秃秃二维码
             colorized=colorful,                          # 背景图是彩色还是黑白
             save_name=outputfile,                              # 保存图片
             )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--content',required=True,help='link or English text')
    parser.add_argument('--bg',default=None,help='background picture')
    parser.add_argument('--outputfile',required=True,help='output filename of generated QRcode')
    parser.add_argument('--colorful', default=True, help='RGB or binary')
    args = parser.parse_args()
    content = args.content
    outputfile = args.outputfile
    bg = args.bg
    colorful = (args.colorful=='True')  # 或者使用action='store_true'
    createQRcode(content,outputfile,bg,colorful)