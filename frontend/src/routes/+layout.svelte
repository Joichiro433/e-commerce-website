<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { isLogin } from '$lib/stores/loginStatus.js';
  import { cartQty, getCartTotalQuantity } from '$lib/stores/cartStatus';
  import Header from '$lib/components/header.svelte';
  import Api from '$lib/api';
  import logger from '$lib/logger';

  let searchQuery: string = $page.params.query ? $page.params.query : '';
  let username: string = '';

  $: if ($isLogin && !username) {
    fetchUsername();
    getCartTotalQuantity();
  }

  const fetchUsername = async (): Promise<void> => {
    try {
      const resp = await Api.get<User>('/user');
      username = resp.data.email;
    } catch (e) {
      if (Api.verifyAxiosError(e) && e.response?.status === 401) {
        $isLogin = false;
      } else {
        logger.error(e, 'Failed to fetchUsername');
      }
    }
  };

  const handleSearch = (): void => {
    goto(`/1/${searchQuery}`);
  };

  const goToPage = (url: string): void => {
    searchQuery = '';
    goto(url);
  };
</script>

<Header>
  <form class="search-box">
    <input type="text" placeholder="Search for Products" bind:value={searchQuery} />
    <button on:click|preventDefault={handleSearch}><i class="fas fa-search" /></button>
  </form>
  <ul>
    <li>
      <a class:active={$page.url.pathname === '/'} href="/" on:click|preventDefault={() => goToPage('/')}>
        <i class="fa-solid fa-shop" /> Store
      </a>
    </li>
    {#if $isLogin}
      <li>
        <a class:active={$page.url.pathname === '/orders'} href="/orders">
          <i class="fa-solid fa-clock" /> Orders
        </a>
      </li>
    {/if}
    {#if $isLogin}
      <li>
        <a class:active={$page.url.pathname === '/mypage'} href="/mypage">
          <i class="fa-solid fa-user" />
          {username.length > 13 ? `${username.substring(0, 10)}...` : username}
        </a>
      </li>
    {:else}
      <li>
        <a class:active={$page.url.pathname === '/login'} href="/login">
          <i class="fa-solid fa-door-closed" /> Login
        </a>
      </li>
    {/if}
    <li>
      <a class:active={$page.url.pathname === '/cart'} href="/cart">
        <i class="fa-solid fa-cart-shopping" /> Cart ({$cartQty})
      </a>
    </li>
  </ul>
</Header>

<main class="container" style="padding-top: 80px;">
  <slot />
</main>

<style>
  ul {
    margin: 0;
    margin-top: 14%;
    padding: 0;
    height: 90vh;
  }

  li {
    margin-left: 1rem;
    height: 10%;
    list-style: none;
  }

  a.active {
    color: #ff0084;
  }

  .search-box {
    display: flex;
    max-width: 50rem; /* 最大の横幅を50remに設定 */
    width: 100%; /* 横幅を100%に設定して、コンテナの幅に合わせる */
    margin: 0 auto; /* センタリングのためのスタイル */
  }

  .search-box input {
    padding: 0rem 0.5rem;
    margin-top: 1.5rem;
    outline: none;
  }

  .search-box button {
    padding: 0rem 1rem;
    margin-top: 1.5rem;
    /* background-color: #333; */
    color: #fff;
    cursor: pointer;
  }

  @media screen and (min-width: 50rem) {
    ul {
      margin-top: 0;
      display: -webkit-box;
      display: -ms-flexbox;
      display: flex;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      height: auto;
    }
    li {
      margin-bottom: 0;
      margin-left: 2rem;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      height: auto;
    }
    li {
      margin-bottom: 0;
      margin-left: 2rem;
    }
    a {
      opacity: 1;
    }
    .search-box {
      position: static;
      transform: none;
      grid-column: 2/3;
      margin: 0 auto;
    }
  }
</style>
