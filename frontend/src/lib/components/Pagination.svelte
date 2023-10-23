<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import Api from '$lib/api';
  import { PRODUCTS_LIMIT_TO_SHOW } from '$lib/constants';

  export let currentPage: number;
  export let query: string;

  let totalPages: number;

  const handlePage = (page: number) => {
    goto(`/${page}/${query}`);
  };

  const getVisiblePageNumbers = (): number[] => {
    let startPage: number;
    let endPage: number;

    if (currentPage <= 3) {
      startPage = 1;
      endPage = 5;
    } else if (currentPage > totalPages - 2) {
      startPage = totalPages - 4;
      endPage = totalPages;
    } else {
      startPage = currentPage - 2;
      endPage = currentPage + 2;
    }

    const visiblePages: number[] = Array.from({ length: endPage - startPage + 1 }, (_, i) => i + startPage);
    return visiblePages;
  };

  const getTotalPages = async () => {
    try {
      const resp = await Api.get<ProductsCount>('/products/count');
      const productsCount = resp.data.count;
      totalPages = Math.ceil(productsCount / PRODUCTS_LIMIT_TO_SHOW);
    } catch (e) {
      console.error('Error fetching products count:', e);
    }
  };

  onMount(getTotalPages);
</script>

<div class="pagination">
  <button on:click={() => handlePage(currentPage - 1)} disabled={currentPage === 1}>&lt;&lt;</button>
  {#each getVisiblePageNumbers() as pageNumber (pageNumber)}
    <button on:click={() => handlePage(pageNumber)} class={pageNumber === currentPage ? 'active' : ''}
      >{pageNumber}</button
    >
  {/each}
  <button on:click={() => handlePage(currentPage + 1)} disabled={currentPage === totalPages}>&gt;&gt;</button>
</div>

<style>
  .pagination {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 2rem 0;
  }

  .pagination button {
    padding: 8px 12px;
    border: none;
    background-color: #d1d1d1;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .pagination button:hover {
    background-color: rgba(155, 77, 202, 0.1);
  }

  .pagination button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  .pagination button.active {
    background-color: #9b4dca;
    color: white;
  }
</style>
