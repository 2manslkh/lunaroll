import mkcert from 'vite-plugin-mkcert';
import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit(), mkcert()],
	server: {
		https: true,
		proxy: {}
	},
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
};

export default config;
