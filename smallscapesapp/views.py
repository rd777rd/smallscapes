import time

from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .models import Review

# Minimum seconds a visitor must spend on the review form before a submission
# is accepted. Bots that fetch-and-POST immediately are rejected; this needs
# no external service and no extra dependency.
MIN_FORM_FILL_SECONDS = 3


def logout_view(request):
    django_logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def projects(request):
    return render(request, 'projects.html')


def review_list(request):
    # Auto-seed standard reviews if the database table is completely empty
    # (fresh install / demo environments only).
    if not Review.objects.exists():
        Review.objects.create(
            name="Marcus Vance", rating=5, is_approved=True,
            comment="SmallScapes did an outstanding job laying brick pavers for our backyard patio. Their craftsmanship is exceptionally precise, level, and they completed the work right on schedule! The slope grading was perfectly plotted, and we have had zero drainage issues during heavy central Indiana rains."
        )
        Review.objects.create(
            name="Evelyn Miller", rating=5, is_approved=True,
            comment="I can't say enough good things about Rom and his crew. They transformed our overgrown garden pathway into a gorgeous flat flagstone walkway with crisp steel borders. Clean, polite, and extremely focused on physical detail. Worth every penny!"
        )
        Review.objects.create(
            name="Jordan K.", rating=4, is_approved=True,
            comment="Great communication, fair pricing, and clean masonry. The stone seating retaining wall they built is incredibly solid and handles slopes nicely. It has become our preferred gathering spot in the yard."
        )

    # Staff can see pending reviews too (so they know what needs approval);
    # everyone else only sees approved, published reviews.
    if request.user.is_authenticated and request.user.is_staff:
        reviews = Review.objects.all()
        pending_count = Review.objects.filter(is_approved=False).count()
    else:
        reviews = Review.objects.filter(is_approved=True)
        pending_count = 0

    approved_reviews = Review.objects.filter(is_approved=True)
    average_rating = approved_reviews.aggregate(avg=Avg('rating'))['avg']

    return render(request, 'reviews.html', {
        'reviews': reviews,
        'average_rating': round(average_rating, 1) if average_rating else None,
        'review_count': approved_reviews.count(),
        'pending_count': pending_count,
    })


def leave_review(request):
    if request.method == 'POST':
        # Honeypot: a hidden field real visitors never fill in. Bots that
        # blindly fill every input on the form trip this and get silently
        # bounced back to the thank-you-style flow without being stored.
        if request.POST.get('website'):
            return redirect('thank_you')

        # Simple timing check: reject submissions faster than a human could
        # plausibly type a review. No extra dependency, no CAPTCHA required.
        try:
            started_at = float(request.POST.get('form_started_at', 0))
        except (TypeError, ValueError):
            started_at = 0
        if started_at and (time.time() - started_at) < MIN_FORM_FILL_SECONDS:
            return redirect('thank_you')

        name = (request.POST.get('name') or '').strip()
        try:
            rating = int(request.POST.get('rating', 5))
        except (ValueError, TypeError):
            rating = 5
        comment = (request.POST.get('comment') or '').strip()

        if name and comment:
            Review.objects.create(
                name=name[:100],
                rating=min(5, max(1, rating)),
                comment=comment[:2000],
                is_approved=False,  # held for staff review before publishing
            )
            return redirect('thank_you')

    return render(request, 'leave_review.html', {'form_started_at': time.time()})


def thank_you(request):
    return render(request, 'thank_you.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def delete_review(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('review_list')
    review = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'confirm_delete.html', {'review': review})


def approve_review(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('review_list')
    review = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        review.is_approved = True
        review.save(update_fields=['is_approved'])
        messages.success(request, f"Review from {review.name} is now published.")
    return redirect('review_list')
