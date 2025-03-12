handleTemplateLoad({
  name: "counter_template",
  description: "一个简单的React计数器应用示例",
  content: `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>简单计数器应用</title>
  
  <script type="importmap">
    {
      "imports": {
        "react": "https://esm.sh/react@19.0.0",
        "react-dom": "https://esm.sh/react-dom@19.0.0",
        "react-dom/client": "https://esm.sh/react-dom@19.0.0/client"
      }
    }
  </script>
  
  <script type="module" src="https://esm.sh/run"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
  <div id="root"></div>

  <script type="text/babel">
    import React, { useState } from 'react';
    import { createRoot } from 'react-dom/client';
    
    // 计数器组件
    const Counter = () => {
      const [count, setCount] = useState(0);
      
      return (
        <div className="flex flex-col items-center justify-center min-h-screen">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h1 className="text-3xl font-bold text-center mb-6">简单计数器</h1>
            
            <div className="flex items-center justify-center mb-6">
              <span className="text-6xl font-bold text-blue-600">{count}</span>
            </div>
            
            <div className="flex space-x-4">
              <button 
                className="px-6 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
                onClick={() => setCount(count - 1)}
              >
                减少
              </button>
              
              <button 
                className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                onClick={() => setCount(count + 1)}
              >
                增加
              </button>
            </div>
            
            <button 
              className="w-full mt-4 px-6 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors"
              onClick={() => setCount(0)}
            >
              重置
            </button>
          </div>
          
          <p className="mt-8 text-gray-500 text-sm">
            使用多八多AI编辑器创建的简单计数器应用
          </p>
        </div>
      );
    };
    
    // 渲染应用
    const root = createRoot(document.getElementById('root'));
    root.render(<Counter />);
  </script>
</body>
</html>`
}); 