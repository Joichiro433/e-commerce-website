<script lang="ts">
  import { page } from '$app/stores';
  import { PRODUCTS_LIMIT_TO_SHOW } from '$lib/constants';
  import Api from '$lib/api';
  import ProductCard from '$lib/components/ProductCard.svelte';
  import Pagination from '$lib/components/Pagination.svelte';
  import logger from '$lib/logger';

  let products: Product[] = [];
  let currentPage: number;
  let query: string;
  $: {
    currentPage = $page.params.page ? parseInt($page.params.page, 10) : 1;
    query = $page.params.query ? $page.params.query : '';
    getProducts();
  }

  const getProducts = async (): Promise<void> => {
    try {
      const params = { skip: (currentPage - 1) * PRODUCTS_LIMIT_TO_SHOW, limit: PRODUCTS_LIMIT_TO_SHOW, query: query };
      const resp = await Api.get<Product[]>('/products', { params: params });
      products = resp.data;
    } catch (e) {
      logger.error(e, 'Failed to getProducts');
    }
  };
</script>

<div class="product-list">
  {#each products as product (product.id)}
    <ProductCard {product} />
  {/each}
</div>

<Pagination {currentPage} {query} />

<style>
  .product-list {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
  }
</style>
