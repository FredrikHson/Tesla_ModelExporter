/*
 *  not actual code just notes on how to implement the format
 *  everything will be written as a binary format
 * */
#define uint8 unsigned char
#define uint16 unsigned short
#define uint32 unsigned int

enum NodeTypes
{
    Root = 0,
    Transform,
    Object, // containts one or more Meshes
    Mesh,
    VertexArray,
    IndexArray,
    Material
};
struct Header
{
    char magic = "FULHAX";
    Root rootnode;
};

class Node
{
    uint32 size; // how big is it after the base node type size to be able to load it quickly and skip over if needed even if the type is not implemented yet
    uint16 type;
    uint16 numChildren;
    Node* children;
};

class Root: Node
{
    type = Root;
};

class TransformNode: Node
{
    type = Transform;
    float matrix[16];
};

class VertexArray: Node
{
    type = VertexArray;
    uint32 attriblen;
    char attrib[] = "Position"; // or normal,texcoord,.....
    uint8 vertlength = 3; // number of elements per vertex 1-4
    uint32 numelements;
    float Data[numelements]; // float/int/whatever is needed by the vertex array attribute probably just floats
};

class Object: Node
{
    type = Object;
    uint32 numberofmeshes;
    Mesh* meshes[numberofmeshes];
    Material material[numberofmeshes];
};

class Mesh: Node
{
    type = Mesh;
    uint32 numVertexArrays;
    VertexArray* vertexbuffers;
    IndexArray* index;
};

class IndexArray: Node
{
    type = IndexArray;
    uint8 sides = 3; // or 4 if quads should ever be implemented
    uint32 numFaces;
    uint32 index[numFaces * sides];
};

class Material: Node
{
    uint32 len;
    char name[len]; // the actual material with shaders refer to this from script/c++
}
