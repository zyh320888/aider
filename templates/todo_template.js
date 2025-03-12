handleTemplateLoad({
  name: "todo_template",
  description: "一个简单的待办事项管理应用",
  content: `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>多八多待办事项</title>
  
  <script type="importmap">
    {
      "imports": {
        "react": "https://esm.sh/react@19.0.0",
        "react-dom": "https://esm.sh/react-dom@19.0.0",
        "react-dom/client": "https://esm.sh/react-dom@19.0.0/client",
        "@tanstack/react-query": "https://esm.sh/@tanstack/react-query@5.67.1",
        "axios": "https://esm.sh/axios@1.6.2",
        "@d8d-appcontainer/api": "https://esm.sh/@d8d-appcontainer/api@3.0.39"
      }
    }
  </script>
  
  <script type="module" src="https://esm.sh/run"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    import React, { useState, useEffect } from 'react';
    import { createRoot } from 'react-dom/client';
    
    // 待办事项应用
    const App = () => {
      const [todos, setTodos] = useState([]);
      const [input, setInput] = useState('');
      
      useEffect(() => {
        // 从localStorage加载待办事项
        const savedTodos = localStorage.getItem('todos');
        if (savedTodos) {
          setTodos(JSON.parse(savedTodos));
        }
      }, []);
      
      // 保存到localStorage
      useEffect(() => {
        localStorage.setItem('todos', JSON.stringify(todos));
      }, [todos]);
      
      const addTodo = () => {
        if (!input.trim()) return;
        setTodos([...todos, { text: input, completed: false, id: Date.now() }]);
        setInput('');
      };
      
      const toggleTodo = (id) => {
        setTodos(todos.map(todo => 
          todo.id === id ? { ...todo, completed: !todo.completed } : todo
        ));
      };
      
      const deleteTodo = (id) => {
        setTodos(todos.filter(todo => todo.id !== id));
      };
      
      return (
        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden">
            <div className="px-4 py-5 bg-blue-500 text-white">
              <h1 className="text-2xl font-bold text-center">待办事项</h1>
            </div>
            
            <div className="p-4">
              <div className="flex mb-4">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addTodo()}
                  placeholder="添加新任务..."
                  className="flex-1 px-4 py-2 border rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={addTodo}
                  className="px-4 py-2 bg-blue-500 text-white rounded-r hover:bg-blue-600"
                >
                  添加
                </button>
              </div>
              
              <ul className="divide-y divide-gray-200">
                {todos.length === 0 ? (
                  <li className="py-4 text-center text-gray-500">暂无待办事项</li>
                ) : (
                  todos.map(todo => (
                    <li key={todo.id} className="py-3 flex items-center">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => toggleTodo(todo.id)}
                        className="h-5 w-5 text-blue-500"
                      />
                      <span className={\`ml-3 flex-1 \${todo.completed ? 'line-through text-gray-400' : ''}\`}>
                        {todo.text}
                      </span>
                      <button
                        onClick={() => deleteTodo(todo.id)}
                        className="ml-2 text-red-500 hover:text-red-700"
                      >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </li>
                  ))
                )}
              </ul>
            </div>
          </div>
        </div>
      );
    };
    
    // 渲染应用
    const root = createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>`
}); 