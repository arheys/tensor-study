import tensorflow as tf

graph = tf.get_default_graph()

print(graph.get_operations())
sess = tf.Session()

input_value = tf.constant(1.0)
sess.run(input_value)

operations = graph.get_operations()

print(operations[0].node_def)

weight = tf.Variable(0.8)

for op in graph.get_operations(): print(op.name)

output_value = weight * input_value

op = graph.get_operations()[-1]
print(op.name)

for op_input in op.inputs: print(op_input)

init = tf.global_variables_initializer()
sess.run(init)

print(sess.run(output_value))

x = tf.constant(1.0, name='input')
w = tf.Variable(0.8, name='weight')
y = tf.multiply(w, x, name='output')
summary_writer = tf.summary.FileWriter('log_simple_graph', sess.graph)

y_ = tf.constant(0.0)
loss = (y - y_)**2

optim = tf.train.GradientDescentOptimizer(learning_rate=0.025)

grads_and_vars = optim.compute_gradients(loss)
sess.run(tf.global_variables_initializer())
print(sess.run(grads_and_vars[1][0]))

sess.run(optim.apply_gradients(grads_and_vars))
print(sess.run(w))

train_step = tf.train.GradientDescentOptimizer(0.025).minimize(loss)

for i in range(100):
    sess.run(train_step)

print(sess.run(y))

summary_y = tf.summary.scalar('output', y)

summary_writer = tf.summary.FileWriter('log_simple_stats')
sess.run(tf.global_variables_initializer())
for i in range(100):
    summary_str = sess.run(summary_y)
    summary_writer.add_summary(summary_str, i)
    sess.run(train_step)

