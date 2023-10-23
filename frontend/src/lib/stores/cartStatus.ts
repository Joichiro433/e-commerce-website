import { writable } from 'svelte/store';
import Api from '$lib/api';

export const cartQty = writable(0);

export const getCartTotalQuantity = async (): Promise<void> => {
  try {
    const resp = await Api.get<CartProducts>('/cart');
    const quantities: number[] = Object.values(resp.data);

    const total = quantities.reduce((acc, curr) => acc + curr, 0);
    cartQty.set(total);
  } catch (e) {
    console.error('Error fetching cart quantities:', e);
  }
};
