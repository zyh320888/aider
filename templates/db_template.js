handleTemplateLoad({
  name: "db_template",
  description: "一个简单的数据库产品展示应用",
  content: `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>多八多产品展示</title>
  
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
<body class="bg-gray-50">
  <div id="root"></div>

  <script type="text/babel">
    import React, { useState, useEffect } from 'react';
    import { createRoot } from 'react-dom/client';
    import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query';
    import { APIClient } from '@d8d-appcontainer/api';
    
    const queryClient = new QueryClient();
    
    // 数据表名常量
    const TABLE_PREFIX = 'd8d_';
    const TABLE_PRODUCTS = \`\${TABLE_PREFIX}products\`;
    
    // 获取API客户端
    const getApiClient = async () => {
      return await APIClient.getInstance({
        scope: 'user',
        config: {
          serverUrl: 'https://app-server.d8d.fun',
          workspaceKey: 'ws_mphxpy6prf9',
          type: 'http'
        }
      });
    };
    
    // 初始化数据库
    const initDatabase = async () => {
      const apiClient = await getApiClient();
      try {
        // 创建产品表
        await apiClient.database.schema.createTable(TABLE_PRODUCTS, (table) => {
          table.increments('id').primary();
          table.string('name').notNullable();
          table.text('description');
          table.decimal('price', 10, 2).notNullable();
          table.integer('stock').defaultTo(0);
          table.string('image_url');
          table.timestamp('created_at').defaultTo(apiClient.database.fn.now());
          table.timestamp('updated_at').defaultTo(apiClient.database.fn.now());
        });

        // 插入示例数据
        const existingProducts = await apiClient.database.table(TABLE_PRODUCTS).select('*');
        if (!existingProducts || existingProducts.length === 0) {
          await apiClient.database.insert(TABLE_PRODUCTS, [
            {
              name: '智能手表',
              description: '高性能智能手表，支持心率监测、运动追踪等功能',
              price: 1299.00,
              stock: 50,
              image_url: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12'
            },
            {
              name: '无线耳机',
              description: '高音质无线蓝牙耳机，支持降噪功能',
              price: 899.00,
              stock: 100,
              image_url: 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb'
            },
            {
              name: '智能音箱',
              description: '智能语音助手，支持多种智能家居控制',
              price: 599.00,
              stock: 30,
              image_url: 'https://images.unsplash.com/photo-1589492477829-5e65395b66cc'
            }
          ]);
        }
      } catch (error) {
        console.log('表已存在或初始化出错:', error);
      }
    };
    
    // 产品卡片组件
    const ProductCard = ({ product, onAddToCart }) => (
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <img 
          src={product.image_url} 
          alt={product.name}
          className="w-full h-48 object-cover"
        />
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-800">{product.name}</h3>
          <p className="text-gray-600 mt-2 text-sm">{product.description}</p>
          <div className="mt-4 flex justify-between items-center">
            <span className="text-blue-500 font-bold">¥{product.price.toFixed(2)}</span>
            <span className="text-gray-500 text-sm">
              库存: {product.stock}
            </span>
          </div>
          <button
            onClick={() => onAddToCart(product)}
            disabled={product.stock <= 0}
            className={\`mt-4 w-full px-4 py-2 rounded \${
              product.stock > 0 
                ? 'bg-blue-500 text-white hover:bg-blue-600' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }\`}
          >
            {product.stock > 0 ? '加入购物车' : '暂时缺货'}
          </button>
        </div>
      </div>
    );
    
    // 产品列表组件
    const ProductList = () => {
      const [cart, setCart] = useState([]);
      
      // 获取产品列表
      const { data: products, isLoading } = useQuery({
        queryKey: ['products'],
        queryFn: async () => {
          const apiClient = await getApiClient();
          return apiClient.database.table(TABLE_PRODUCTS).select('*');
        }
      });
      
      // 添加到购物车
      const addToCart = (product) => {
        const existingItem = cart.find(item => item.id === product.id);
        
        if (existingItem) {
          setCart(cart.map(item => 
            item.id === product.id 
              ? { ...item, quantity: item.quantity + 1 } 
              : item
          ));
        } else {
          setCart([...cart, { ...product, quantity: 1 }]);
        }
      };
      
      // 从购物车移除
      const removeFromCart = (productId) => {
        setCart(cart.filter(item => item.id !== productId));
      };
      
      // 计算总价
      const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      
      if (isLoading) {
        return (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        );
      }
      
      return (
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-2xl font-bold text-center mb-8">多八多产品展示</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products && products.map(product => (
              <ProductCard 
                key={product.id} 
                product={product}
                onAddToCart={addToCart}
              />
            ))}
          </div>
          
          {cart.length > 0 && (
            <div className="mt-12 bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold mb-4">购物车</h2>
              <div className="divide-y divide-gray-200">
                {cart.map(item => (
                  <div key={item.id} className="py-4 flex justify-between items-center">
                    <div>
                      <h3 className="font-medium">{item.name}</h3>
                      <p className="text-gray-500 text-sm">¥{item.price.toFixed(2)} x {item.quantity}</p>
                    </div>
                    <div className="flex items-center">
                      <span className="font-medium mr-4">¥{(item.price * item.quantity).toFixed(2)}</span>
                      <button 
                        onClick={() => removeFromCart(item.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 flex justify-between items-center border-t border-gray-200 pt-4">
                <span className="text-lg font-bold">总计:</span>
                <span className="text-xl font-bold text-blue-600">¥{totalPrice.toFixed(2)}</span>
              </div>
              <button
                className="mt-6 w-full px-6 py-3 bg-green-500 text-white rounded-md hover:bg-green-600"
              >
                结算
              </button>
            </div>
          )}
        </div>
      );
    };
    
    // 主应用组件
    const App = () => {
      const [isLoading, setIsLoading] = useState(true);
      
      useEffect(() => {
        // 初始化数据库
        const init = async () => {
          try {
            await initDatabase();
          } catch (error) {
            console.error('初始化数据库出错:', error);
          } finally {
            setIsLoading(false);
          }
        };
        
        init();
      }, []);
      
      if (isLoading) {
        return (
          <div className="flex justify-center items-center h-screen">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        );
      }
      
      return <ProductList />;
    };
    
    // 渲染应用
    const root = createRoot(document.getElementById('root'));
    root.render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );
  </script>
</body>
</html>`
}); 