<template>
    <div class="main-right col-span-1 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h3 class="mb-6 text-xl">You may interesting</h3>

                <div class="space-y-4">
                    <div class="flex items-center justify-between" v-for="category in categories" v-bind:key="category.id">
                        <p class="text-xs">
                            <strong>#{{ category.hashtag }}</strong>
                            <br>
                            <span class="text-gray-500">{{ category.occurences }} posts</span>
                        </p>

                        <RouterLink :to="{name: 'categories', params: {'id': category.hashtag}}" class="py-2 px-3 bg-white text-black text-xs bg-white border border-gray-200 rounded-lg hover:bg-gray-200">Explore</RouterLink>
                    </div>
                </div>
            </div>
        </div>
</template>
<script>
import axios from 'axios'


export default (await import('vue')).defineComponent({
    name: 'categories',

    data() {
        return {
            categories: []
        }
    },
    mounted() {
        this.getCategories()
    },
    methods: {
        getCategories() {
            axios
                .get('/post/categories/')
                .then(response => {
                    console.log(response.data)

                    this.categories = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    },
})
</script>