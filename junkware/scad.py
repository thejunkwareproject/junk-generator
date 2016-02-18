
def get_template_scad(shapeData):

    shape1="shape1=supershape(" + "m=" + str(shapeData["m1"]) + ", n1=" + str(shapeData["n11"]) + ", n2=" + str(shapeData["n12"]) + ", n3=" + str(shapeData["n13"]) + ", a=1, b=1),"

    shape2="shape2=supershape(" + "m=" + str(shapeData["m2"]) + ", n1=" + str(shapeData["n21"]) + ", n2=" + str(shapeData["n22"]) + ", n3=" + str(shapeData["n23"]) + ", a=1, b=1),"

    template_scad =   """
include <../make/supershape.scad>
create_supershape();
module create_supershape()
{
    scale([10,10,10])
    RenderSuperShape(
        #SHAPE1#
        #SHAPE2#
        phisteps = 8,
        thetasteps = 64,
        points=false,
        pointcolor=[1,1,1],
        wireframe=false,
        faces=true);
}
"""

    scad = template_scad.replace("#SHAPE1#", shape1).replace("#SHAPE2#", shape2)
    return scad
