import random, os

def generate(height):
    n = 1 << height
    cat = list(range(n - 1))
    random.shuffle(cat)
    return cat

def generate_display(cat, short_course_id):
    n = len(cat)
    with open('data/cat%s.dot' % short_course_id, 'w') as f:
        f.write('digraph G {\n')
        f.write('rankdir=UD\n')
        for i in range(n):
            if 2 * i + 2 <= n:
                f.write('"{}" -> "{}";\n'.format(cat[i], cat[2 * i + 1]))
                f.write('"{}" -> "{}";\n'.format(cat[i], cat[2 * i + 2]))
        f.write('}')
    os.system('dot -Tpng data/cat%s.dot > data/cat%s.png' % (short_course_id, short_course_id))

# generate_display(generate(3))
