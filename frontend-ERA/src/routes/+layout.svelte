<script>
	import '../app.css';
	let { children } = $props();
	import { Navbar, NavBrand, NavUl, NavLi } from 'flowbite-svelte';

</script>

<div class="flex flex-col min-h-screen">
	<header class="flex-none">
		<Navbar class="h-16">
			<NavBrand href="/">
				<!-- <img src="/logo.svg" class="mr-3 h-6 sm:h-9" alt="Logo" /> -->
				<span class="self-center whitespace-nowrap text-xl font-semibold text-black">guardian.ai</span>
			</NavBrand>
			<NavUl>
				<NavLi href="/">Home</NavLi>
			</NavUl>
		</Navbar>
	</header>

	<div class="flex flex-col flex-1 w-full">
		<main class="flex-1 w-full h-full">
			{@render children()}
		</main>

		<footer class="flex-none bg-gray-200 py-6">
			<div class="container mx-auto text-center text-gray-600">
				© {new Date().getFullYear()} guardian.ai. All rights reserved.
			</div>
		</footer>
	</div>
</div>