declare type Product = {
  name: string;
  description: string;
  price: number;
  author: string;
  image_url: string;
  id: string;
};

declare type ProductsCount = {
  count: number;
};

declare type CartProducts = {
  [productId: string]: number;
};

declare type User = {
  id: string;
  email: string;
};

declare type OrderItem = {
  quantity: number;
  product: Product;
};

declare type Order = {
  id: string;
  order_items: OrderItem[];
  purchase_date: string;
};

declare type OrderResp = {
  id: string;
  email: string;
  orders: Order[];
};
