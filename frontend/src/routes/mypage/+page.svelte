<script lang="ts">
  import { onMount } from 'svelte';
  import Modal from '$lib/components/Modal.svelte';
  import Api from '$lib/api';
  import logger from '$lib/logger';

  let user: User;
  let deleteInput: string = '';
  let isModalVisible: boolean = false;

  const fetchUser = async (): Promise<void> => {
    try {
      const resp = await Api.get<User>('/user');
      user = resp.data;
    } catch (e) {
      logger.error(e, 'Failed to fetchUser');
    }
  };

  const handleLogout = async (): Promise<void> => {
    try {
      await Api.post('/logout');
      window.location.href = '/';
    } catch (e) {
      logger.error(e, 'Failed to handleLogout');
      alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
    }
  };

  const handleUserDeletion = async (): Promise<void> => {
    if (deleteInput !== 'delete') return;
    try {
      await Api.delete('/user');
      isModalVisible = true;
    } catch (e) {
      logger.error(e, 'Failed to handleUserDeletion');
      alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
    }
  };

  const closeModal = (): void => {
    isModalVisible = false;
    window.location.href = '/';
  };

  onMount(fetchUser);
</script>

{#if user}
  {#if isModalVisible}
    <Modal {closeModal}>
      <h3>ユーザーを削除しました。</h3>
    </Modal>
  {/if}

  <div class="user-profile">
    <h2>ユーザー情報</h2>
    <p>Email: {user.email}</p>
    <button on:click|preventDefault={handleLogout}>ログアウト</button>
    <details>
      <summary>設定</summary>
      <ul>
        <li>
          ユーザー削除
          <div style="color: red;">ユーザーは完全に削除され復元することはできません。</div>
          <div>ユーザーを削除するには「delete」と入力して削除ボタンを押してください。</div>
          <br />
          <input class="delete-input" type="text" bind:value={deleteInput} placeholder="deleteを入力" />
          <button class="delete-button" on:click|preventDefault={handleUserDeletion} disabled={deleteInput !== 'delete'}
            >削除</button
          >
        </li>
      </ul>
    </details>
  </div>
{:else}
  <p>Loading...</p>
{/if}

<style>
  .user-profile {
    max-width: 500px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #f1f1f1;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #f1f1f1;
    padding-bottom: 0.5rem;
  }

  p {
    margin-bottom: 1.5rem;
    color: #333;
  }

  details {
    /* border: 1px solid #aaa; */
    border-radius: 4px;
    padding: 0.5em 0.5em 0;
    margin-top: 20px;
  }

  summary {
    /* font-weight: bold; */
    margin: -0.5em -0.5em 0;
    padding: 0.5em;
  }

  details[open] {
    padding: 0.5em;
  }

  details[open] summary {
    border-bottom: 1px solid #aaa;
    margin-bottom: 0.5em;
  }

  .delete-input {
    width: 200px;
    height: 30px;
    padding: 5px 10px;
    font-size: 0.9em;
    margin: 0px;
    display: inline-block;
    vertical-align: middle;
  }

  .delete-button {
    height: 30px;
    padding: 5px 15px;
    font-size: 0.9em;
    background-color: #d63e57;
    margin: 0px;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    display: inline-block;
    vertical-align: middle;
    line-height: 20px;
  }

  .delete-button:disabled {
    background-color: grey;
  }
</style>
