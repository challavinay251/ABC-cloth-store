from django.shortcuts import render, get_object_or_404, redirect
from .models import Design, Collection, Review, Order
from .forms import OrderForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    designs = Design.objects.all()
    return render(request, 'store/home.html', {'designs': designs})

def collections_by_design(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    collections = design.collections.all()
    return render(request, 'store/design_collection.html', {'design': design, 'collections': collections})

def order_success(request):
    return render(request, 'store/order_success.html')

def design_collection(request):
    designs = Design.objects.all()
    return render(request, 'store/designs.html', {'designs': designs})

@login_required
def add_review(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    review_form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.collection = collection
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('collection_detail', collection_id=collection.id)

    context = {
        'collection': collection,
        'review_form': review_form,
    }
    return render(request, 'store/collection_detail.html', context)

def collection_detail(request, collection_id):
    # Get the specific collection by ID
    collection = get_object_or_404(Collection, id=collection_id)
    reviews = Review.objects.filter(collection=collection)

    # Initialize forms
    order_form = OrderForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        # Handling Order Submission
        if 'order' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                # Add collection to the order form
                order = order_form.save(commit=False)
                order.collection = collection  # Set the collection manually
                order.user = request.user  # Ensure the logged-in user is associated with the order
                order.save()
                messages.success(request, "Your order has been placed successfully!")
                return redirect('order_success')  # Redirect to order success page

        # Handling Review Submission
        elif 'review' in request.POST:
            if request.user.is_authenticated:
                review_form = ReviewForm(request.POST)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.collection = collection
                    review.user = request.user
                    review.save()
                    messages.success(request, "Your review has been submitted!")
                    return redirect('collection_detail', collection_id=collection.id)
            else:
                messages.error(request, "You need to log in to submit a review.")
                return redirect('login')  # Redirect to login if the user is not authenticated

    # Pass forms and collection details to the template
    context = {
        'collection': collection,
        'reviews': reviews,
        'order_form': order_form,
        'review_form': review_form,
    }
    return render(request, 'store/collection_detail.html', context)

# Additional views for adding/deleting reviews
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user.is_staff or request.user == review.user:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this review.")
    return redirect('collection_detail', collection_id=review.collection.id)
