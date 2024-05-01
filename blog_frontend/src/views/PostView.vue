<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-if="post.id">
                <FeedItem v-bind:post="post" />
            </div>
            <div class="p-4 ml-6 bg-white border border-gray-200 rounded-lg" v-for="comment in post.comments" v-bind:kАey="comment.id">
                 <CommentItem v-bind:comment="comment"/>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-2">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What do you think?"></textarea>
                    </div>

                    <div class="p-2 border-t border-gray-100">

                        <button class="inline-block py-2 px-4 text-black bg-white border border-gray-200 rounded-lg hover:bg-gray-200">Post</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <MayInteresting />
        </div>
    </div>
</template>

<script>
import MayInteresting from '../components/MayInteresting.vue'
import axios from 'axios'
import FeedItem from '../components/FeedItem.vue'
import CommentItem from '../components/CommentItem.vue'


export default (await import('vue')).defineComponent({
    name: 'PostView',
    components: {
        MayInteresting,
        FeedItem,
        CommentItem,
    },
    data() {
        return {
            post: {
                id: null,
                comments: [],
            },
            body: '',
        }
    },
    mounted() {
        this.getPost()
    },
    methods: {
        getPost() {
            axios
                .get(`/post/${this.$route.params.id}`)
                .then(response => {
                    console.log('data from post', response.data)
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        submitForm() {
            console.log('submitForm', this.body)

            axios
                .post(`/post/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.post.comments.unshift(response.data)
                    this.post.comments_count = parseInt(this.post.comments_count + 1)
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    },
})
</script>