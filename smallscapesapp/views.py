from django.shortcuts import render, redirect, get_object_or_404
from .models import Review

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'projects.html')

def review_list(request):
    # Auto-seed standard reviews if database table is completely raw
    if not Review.objects.exists():
        Review.objects.create(
            name="Marcus Vance",
            rating=5,
            comment="SmallScapes did an outstanding job laying brick pavers for our backyard patio. Their craftsmanship is exceptionally precise, level, and they completed the work right on schedule! The slope grading was perfectly plotted, and we have had zero drainage issues during heavy central Indiana rains."
        )
        Review.objects.create(
            name="Evelyn Miller",
            rating=5,
            comment="I can't say enough good things about Rom and his crew. They transformed our overgrown garden pathway into a gorgeous flat flagstone walkway with crisp steel borders. Clean, polite, and extremely focused on physical detail. Worth every penny!"
        )
        Review.objects.create(
            name="Jordan K.",
            rating=4,
            comment="Great communication, fair pricing, and clean masonry. The stone seating retaining wall they built is incredibly solid and handles slopes nicely. It has become our preferred gathering spot in the yard."
        )

    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})

def leave_review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            rating = int(request.POST.get('rating', 5))
        except (ValueError, TypeError):
            rating = 5
        comment = request.POST.get('comment')
        
        if name and comment:
            Review.objects.create(
                name=name,
                rating=min(5, max(1, rating)),
                comment=comment
            )
            return redirect('thank_you')
            
    return render(request, 'leave_review.html')

def thank_you(request):
    return render(request, 'thank_you.html')

def delete_review(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('review_list')
    review = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'confirm_delete.html', {'review': review})
