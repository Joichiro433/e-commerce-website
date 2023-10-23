<script lang="ts">
  import { onMount } from 'svelte';
  import Api from '$lib/api';
  import logger from '$lib/logger';
  import OrderTable from '$lib/components/OrderTable.svelte';

  let ordersGroupedByDate: Record<string, Order[]> = {};

  const fetchAndGroupOrdersByDate = async (): Promise<void> => {
    try {
      const resp = await Api.get<OrderResp>('/orders');
      const fetchedOrders: Order[] = resp.data.orders;

      // Group orders by purchase_date (without time)
      fetchedOrders.forEach((order) => {
        const dateOnly = order.purchase_date.split('T')[0]; // Extract only the date part

        if (!ordersGroupedByDate[dateOnly]) {
          ordersGroupedByDate[dateOnly] = [];
        }
        ordersGroupedByDate[dateOnly].push(order);
      });
    } catch (e) {
      logger.error(e, 'Failed to fetchAndGroupOrdersByDate');
    }
  };

  onMount(fetchAndGroupOrdersByDate);
</script>

<h1>購入履歴</h1>

{#each Object.keys(ordersGroupedByDate).sort().reverse() as date}
  <div class="order-date">
    <h3>注文日: {new Date(date).toLocaleDateString('ja-JP', { year: 'numeric', month: 'numeric', day: 'numeric' })}</h3>
    {#each ordersGroupedByDate[date] as order}
      <OrderTable {order} />
    {/each}
  </div>
{/each}

<style>
  .order-date {
    border: 1px solid #ccc;
    margin-bottom: 16px;
    padding: 16px;
  }
</style>
