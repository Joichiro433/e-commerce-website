<script lang="ts">
  export let order: Order;

  const calculateTotal = (orderItems: OrderItem[]): number => {
    return orderItems.reduce((acc, item) => acc + item.product.price * item.quantity, 0);
  };
</script>

<div class="order">
  <h5>注文ID: {order.id}</h5>
  <table>
    <thead>
      <tr>
        <th />
        <th>商品名</th>
        <th>購入数</th>
        <th>金額 / 個</th>
      </tr>
    </thead>
    <tbody>
      {#each order.order_items as item}
        <tr>
          <td><img src={item.product.image_url} alt={item.product.name} class="product-image" /></td>
          <td>{item.product.name}</td>
          <td>{item.quantity} 個</td>
          <td>¥ {item.product.price.toLocaleString()}</td>
        </tr>
      {/each}
    </tbody>
  </table>
  <div class="subtotal">小計: ¥ {calculateTotal(order.order_items).toLocaleString()}</div>
</div>

<style>
  .order {
    margin-top: 16px;
  }

  .product-image {
    width: 60px;
    vertical-align: middle;
    margin-right: 8px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th,
  td {
    padding: 8px 12px;
  }

  tr:not(:last-child) {
    border-bottom: 1px solid #ddd;
  }

  th {
    background-color: #f2f2f2;
  }

  table th:nth-child(1),
  table td:nth-child(1) {
    width: 100px;
  }

  table th:nth-child(2),
  table td:nth-child(2) {
    width: calc(100% - 100px - 80px - 90px); /* 画像と購入数、金額のセルの幅を除いたもの */
  }

  table th:nth-child(3),
  table td:nth-child(3),
  table th:nth-child(4),
  table td:nth-child(4) {
    width: 90px;
  }

  .subtotal {
    text-align: right;
    margin-top: 12px;
    font-weight: bold;
  }
</style>
