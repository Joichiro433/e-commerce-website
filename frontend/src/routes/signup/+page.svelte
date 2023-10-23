<script lang="ts">
  import { goto } from '$app/navigation';
  import Api from '$lib/api';
  import Modal from '$lib/components/Modal.svelte';
  import logger from '$lib/logger';

  let email: string = '';
  let password: string = '';
  let isModalVisible: boolean = false;

  const handleSignup = async (): Promise<void> => {
    const data = {
      email: email,
      password: password,
    };
    try {
      await Api.post('/signup', data);
      isModalVisible = true;
    } catch (e) {
      logger.error(e, 'Failed to handleSignup');
      alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
    }
  };

  const closeModal = (): void => {
    isModalVisible = false;
    goto('/login');
  };
</script>

{#if isModalVisible}
  <Modal {closeModal}>
    <h3>ユーザーを作成しました！</h3>
    <p>ログインページでログインしてください。</p>
  </Modal>
{/if}

<form>
  <h2>Sign Up</h2>
  <div>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required bind:value={email} />
  </div>

  <div>
    <label for="password">Password:</label>
    <input type="password" id="password" name="password" required bind:value={password} />
  </div>

  <div>
    <button type="submit" on:click|preventDefault={handleSignup}>Sign Up</button>
  </div>

  <div>
    <p style="text-align: center;">
      Already have an account?
      <a href="/login" on:click|preventDefault={() => goto('/login')}>Log In</a>
    </p>
  </div>
</form>

<style>
  form {
    max-width: 400px;
    margin: 4rem auto;
    padding: 2rem;
    border: 1px solid #f1f1f1;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h2 {
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #9b4dca;
  }

  div {
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }

  input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  a {
    color: #9b4dca;
    text-decoration: underline;
    cursor: pointer;
  }
</style>
