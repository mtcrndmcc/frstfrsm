import bext, random, enum

bext.bg( "black" )

k_tree_chr = 'A'
k_fire_chr = 'W'

width, height = bext.size( )
area = width * height

def input_chance( arg ):
    out = 0

    try:
        out = int( arg )
    except:
        print( "invalid arg!" )
        exit( )
    
    if out <= 0 or out > 100:
        print( "invalid arg!" )
        exit( )

    return out

chance_to_grow = 100 - input_chance( input( "chance_to_grow ( 1 - 100 ) = ") )
chance_to_fire = 100 - input_chance( input( "chance_to_fire ( 1 - 100 ) = ") )

class e_cell_type( enum.Enum ):
    undefined   = -1,
    empty       = 0,
    tree        = 1,
    fire        = 2
    
g_cells = [ e_cell_type.empty ] * area

def simulate( ):
    new_cells = [ e_cell_type.undefined ] * area

    for x in range( width ):
        for y in range( height ):
            pos = x + width * y
            if new_cells[ pos ] != e_cell_type.undefined:
                continue
            
            if g_cells[ pos ] == e_cell_type.empty:
                new_cells[ pos ] = e_cell_type.tree if chance_to_grow <= 0 or random.randint( 0, 100 ) >= chance_to_grow else g_cells[ pos ]
            elif g_cells[ pos ] == e_cell_type.tree:
                new_cells[ pos ] = e_cell_type.fire if chance_to_fire <= 0 or random.randint( 0, 100 ) >= chance_to_fire else g_cells[ pos ]
            elif g_cells[ pos ] == e_cell_type.fire:
                for i in range( -1 if x > 0 else 0, 2 if x < ( width - 1 ) else 1 ):
                    for j in range( -1 if y > 0 else 0, 2 if y < ( height - 1 ) else 1 ):
                        next_pos = ( x + i ) + width * ( y + j )
                        if g_cells[ next_pos ] == e_cell_type.tree:
                            new_cells[ next_pos ] = e_cell_type.fire

                new_cells[ pos ] = e_cell_type.empty
    
    return new_cells

def render( ):
    bext.goto( 0, 0 )

    for cell in g_cells:
        if cell == e_cell_type.empty:
            bext.fg( "white" )
            print( " ", end="" )
        elif cell == e_cell_type.tree:
            bext.fg( "green" )
            print( k_tree_chr, end="" )
        elif cell == e_cell_type.fire:
            bext.fg( "red" )
            print( k_fire_chr, end="" )

try:
    bext.clear( )

    while True:
        g_cells = simulate( )

        render( )
except KeyboardInterrupt:
    pass